# MetaTune engine : blend a few games into one mood and recommend real songs for it.
# No RapidAPI here : the game features were already collected once in
# data/rapidapi_features_clean.csv, and the real songs come from a public
# Spotify audio-features dataset (kagglehub, or a local csv cache).

import os
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

features = ["danceability", "energy", "valence", "acousticness",
            "instrumentalness", "liveness", "speechiness", "tempo"]

ROOT = Path(__file__).resolve().parent.parent
OST_CSV = ROOT / "data" / "rapidapi_features_clean.csv"
SONGS_CSV = ROOT / "data" / "external" / "spotify_tracks_hf.csv"


class MetaTune:

    def __init__(self, ost_csv=OST_CSV, songs_csv=SONGS_CSV):
        ost = pd.read_csv(ost_csv).dropna(subset=features).copy()
        songs = self._load_songs(songs_csv)

        # OST features are on a 0-100 scale, Spotify on 0-1, so I divide everything
        # except tempo (BPM in both) by 100 before mixing the two
        pct = [f for f in features if f != "tempo"]
        ost[pct] = ost[pct] / 100.0

        # one scaler fit on both so games and songs end up in the same space
        self.scaler = MinMaxScaler().fit(pd.concat([ost[features], songs[features]]))
        ost_scaled = self.scaler.transform(ost[features])
        self.songs = songs
        self.songs_scaled = self.scaler.transform(songs[features])

        # a game's signature = the mean of its scaled tracks
        self.signatures = {g: ost_scaled[(ost.game_title == g).values].mean(axis=0)
                           for g in ost.game_title.unique()}

    def _load_songs(self, songs_csv):
        songs_csv = Path(songs_csv)
        if songs_csv.exists():
            songs = pd.read_csv(songs_csv)
        else:
            # not downloaded yet, grab it from Kaggle once and cache it
            import kagglehub
            path = kagglehub.dataset_download("maharshipandya/-spotify-tracks-dataset")
            songs = pd.read_csv(os.path.join(path, "dataset.csv"))
            songs_csv.parent.mkdir(parents=True, exist_ok=True)
            songs.to_csv(songs_csv, index=False)

        songs = songs.dropna(subset=features)
        # the dataset repeats a song once per genre, so I keep one row per song (the most popular)
        return (songs.sort_values("popularity", ascending=False)
                     .drop_duplicates(subset=["track_name", "artists"])
                     .reset_index(drop=True))

    @property
    def games(self):
        return sorted(self.signatures)

    def mood(self, weights):
        # weighted average of the game signatures (weights don't have to sum to 1)
        total = sum(weights.values())
        vec = np.zeros(len(features))
        for game, w in weights.items():
            vec += (w / total) * self.signatures[game]
        return vec

    def recommend(self, weights, top_n=15, min_popularity=10, lam=0.7, pool_size=250):
        mood = self.mood(weights)

        # only keep songs above the popularity I asked for
        mask = (self.songs.popularity >= min_popularity).values
        pool = self.songs[mask].reset_index(drop=True)
        pool_scaled = self.songs_scaled[mask]

        # closest songs to the mood
        sims = cosine_similarity(pool_scaled, mood.reshape(1, -1)).ravel()
        order = sims.argsort()[::-1][:pool_size]
        pool, pool_scaled, sims = pool.iloc[order].reset_index(drop=True), pool_scaled[order], sims[order]

        # MMR re-rank so I don't get 15 near-identical tracks : relevance (lam) vs diversity
        chosen, left = [], list(range(len(pool_scaled)))
        while len(chosen) < top_n and left:
            if not chosen:
                best = left[np.argmax(sims[left])]
            else:
                rest = np.array(left)
                redundancy = cosine_similarity(pool_scaled[rest], pool_scaled[chosen]).max(axis=1)
                best = int(rest[np.argmax(lam * sims[rest] - (1 - lam) * redundancy)])
            chosen.append(best)
            left.remove(int(best))

        out = pool.iloc[chosen].copy()
        out["sim"] = sims[chosen]
        return out[["track_name", "artists", "track_genre", "popularity", "track_id", "sim"]]

    def to_m3u(self, tracks, path):
        # M3U I can import into Spotify with Soundiiz / TuneMyMusic
        lines = ["#EXTM3U"]
        for _, r in tracks.iterrows():
            lines.append(f"#EXTINF:-1,{r['artists']} - {r['track_name']}")
            lines.append(f"https://open.spotify.com/track/{r['track_id']}")
        Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def to_spotify(self, tracks, name="MetaTune Recommendations"):
        # push the tracks into a real playlist (user OAuth flow, same as notebook 06)
        import spotipy
        from spotipy.oauth2 import SpotifyOAuth
        from spotipy.exceptions import SpotifyException

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-modify-private playlist-modify-public",
            cache_path=".cache-user",
        ))
        uris = [f"spotify:track:{t}" for t in tracks["track_id"]]
        try:
            pl = sp.current_user_playlist_create(name=name, public=False,
                                                 description="Generated by MetaTune")
            for i in range(0, len(uris), 100):
                sp.playlist_add_items(pl["id"], uris[i:i + 100])
            return pl["external_urls"]["spotify"]
        except SpotifyException as e:
            # apps in dev mode get a 403 on writes, fall back to the m3u file
            if e.http_status == 403:
                print("Spotify said 403 (app in dev mode), use to_m3u + Soundiiz instead.")
                return None
            raise


if __name__ == "__main__":
    mt = MetaTune()
    blend = {"Stardew Valley": 0.6, "Detroit: Become Human": 0.4}
    print(len(mt.games), "games |", blend)
    print(mt.recommend(blend, top_n=10).to_string(index=False))
