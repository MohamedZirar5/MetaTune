# 🎧 MetaTune: The Beat of Your Gameplay

Hi, I'm Mohamed Zirar, third year Computer Science student, and future Data Scientist!
**MetaTune** is a Data Science project born from my love for video game original soundtracks (OSTs). After finishing a game or spending hours in its world, I often listen to the OST on loop.

This GitHub repo shows the full thinking process behind the project, not just the final code. It includes the data sourcing decisions, the legal checks, the API tradeoffs, and the notebook work that led to the current pipeline.

This project answers the question:
**"How can I find songs that match the vibe of a specific game or, even better, a blend of multiple games I'm playing?"**

While many users create these playlists manually, they are often biased toward individual taste. As an incoming Data Science Master's student and long-time gamer, I wanted to build an automated music recommender that bridges the gap between gaming and music through data.

## The Core Idea: Multi-Atmosphere Fusion
Most recommenders analyze one source at a time. **MetaTune** lets you blend several games into one mood. I call those "meta-moods".

Want the cozy farm life of *Stardew Valley* mixed with the cold sci-fi tension of *Detroit: Become Human*? The engine averages each game's audio "signature" into a **Mood Centroid** (the sweet spot between those worlds), then recommends **real songs**, real artists, not just other game soundtracks, that sit closest to it.

## Project Roadmap
- [x] *Phase 1:* Track discovery with `Spotify` and audio features via `RapidAPI` (after Spotify deprecated the audio-features endpoint).
(https://rapidapi.com/soundnet-soundnet-default/api/track-analysis)
- [x] *Phase 2:* Merging several game profiles into one "target vibe" with weighted averages (the meta-mood).
- [x] *Phase 3:* `MinMaxScaler` for normalization, then ranking tracks by cosine similarity, with AGNES clustering + MMR re-ranking to keep the playlist varied.
- [x] *Phase 4:* Recommending **real (non-OST) songs** from a public Spotify audio-features dataset, no RapidAPI fetching needed.
- [x] *Phase 5:* Exporting the result as a playlist (an M3U file, or straight into a Spotify playlist through the API).
- [ ] *Phase 6:* Interactive Radar Charts to visualize how well a recommended song overlaps the mood.

## How it works

- Identify game titles (Steam Web API / a manual seed list) and map them to soundtrack albums via `spotipy`.
- Collect the 8 audio features (danceability, energy, valence, acousticness, instrumentalness, liveness, speechiness, tempo) for each OST track through RapidAPI, cached under `data/`.
- Average each game's tracks into a "sound signature", then blend several signatures into one weighted mood centroid.
- For the real-music recommendations, reuse a public Spotify audio-features dataset (114k songs, pulled with `kagglehub`) so I don't have to fetch anything, harmonize its 0–1 scale with the OST 0–100 features, and rank songs by cosine similarity + MMR.
- Export the playlist to an M3U file or push it straight to Spotify.
- Keep API keys out of the repo (`.env`).

## Tech Stack
*   **Data Science:** Pandas & NumPy
*   **Machine Learning:** Scikit-Learn (`MinMaxScaler`, AGNES clustering, cosine similarity, MMR)
*   **Data:** `kagglehub` (public Spotify audio-features dataset), RapidAPI Track Analysis (OST features)
*   **APIs:** Spotipy for Spotify search, album discovery and playlist export
*   **Visuals:** Plotly / Matplotlib

## Structure
*   `/data`: cached audio features (game OSTs) and the public song dataset.
*   `/notebooks`: the "lab", 01–04 build the dataset and clustering, 05 recommends real songs for a game blend, 06 exports the playlist to Spotify.
*   `/src`: the recommendation engine (`engine.py` → the `MetaTune` class).

## Using the engine

```python
from src.engine import MetaTune

mt = MetaTune()
tracks = mt.recommend({"Stardew Valley": 0.6, "Detroit: Become Human": 0.4})
mt.to_m3u(tracks, "data/metamood.m3u8")   # import into Spotify via Soundiiz
# mt.to_spotify(tracks)                    # or push straight to a Spotify playlist
```

Note: I cleared the output of the first 2 notebooks so I don’t leak my IDs or the raw RapidAPI data. For the rest, I left the outputs in place so you can see the analysis and results.

---

*Created by an aspiring Data Scientist who spends way too much time thinking about game aesthetics. This project explores API integration and the use of math to model the subjective beauty of music.*