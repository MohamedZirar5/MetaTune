# 🎧 MetaTune: The Beat of Your Gameplay

Hi, I'm Mohamed Zirar, third year Computer Science student, and future Data Scientist!
**MetaTune** is a Data Science project born from my love for video game original soundtracks (OSTs). After finishing a game or spending hours in its world, I often listen to the OST on loop.

This GitHub repo shows the full thinking process behind the project, not just the final code. It includes the data sourcing decisions, the legal checks, the API tradeoffs, and the notebook work that led to the current pipeline.

This project answers the question:
**"How can I find songs that match the vibe of a specific game or, even better, a blend of multiple games I'm playing?"**

While many users create these playlists manually, they are often biased toward individual taste. As an incoming Data Science Master's student and long-time gamer, I wanted to build an automated music recommender that bridges the gap between gaming and music through data.

## The Core Idea: Multi-Atmosphere Fusion
Most recommenders analyze one source at a time. **MetaTune** allows you to blend multiple games that currently matches your mood. We'll call those "meta-moods"

Want the epic, orchestral scale of *The Legend of Zelda* mixed with the gritty, industrial anxiety of *Lethal Company*? The engine calculates a **Mood Centroid**—a mathematical "sweet spot" between these worlds—to find tracks that sit at the intersection of your favorite games.

## Project Roadmap
- [x] *Phase 1:* Leveraging `Spotify` for track discovery and `RapidAPI` for redirected audio analysis after Spotify deprecated the audio-features endpoint.
(https://rapidapi.com/soundnet-soundnet-default/api/track-analysis)
- [ ] *Phase 2:* Building a vector-based aggregator that merges multiple game profiles into a single "target vibe" using weighted averages.
- [ ] *Phase 3:* Implementing `MinMaxScaler` for data normalization and using Euclidean Distance to rank the tracks that are "closest" to the game's atmosphere.
- [ ] **Phase 4:* Creating interactive Radar Charts to visualize how well a recommended song overlaps with the game's profile.

## What we'll do here

- Use the Steam Web API (or a manual seed list) to identify game titles and verify `appid`s.
- Map games to soundtrack albums via `spotipy` (Spotify search) and resolve album/track IDs.
- Use a Track Analysis API (RapidAPI / SoundNet) to collect audio features (danceability, energy, valence/happiness, acousticness, instrumentalness, liveness, speechiness, tempo, etc.).
- Cache API results locally under `data/` to avoid re-querying and respect rate limits.
- Aggregate track features per game to compute a mood centroid and produce music recommendations.
- Keep API keys out of the repo (`.env`) and do not store personal Steam data unless explicitly consented.

## Tech Stack
*   **Data Science:** Pandas & NumPy
*   **Machine Learning:** Scikit-Learn (`MinMaxScaler`, Similarity Metrics)
*   **APIs:** Spotipy for Spotify search and album discovery, RapidAPI Track Analysis for redirected audio features
*   **Visuals:** Plotly / Matplotlib

## Structure
*   `/data`: The "Sound Signatures" curated datasets of audio features.
*   `/notebooks`: Experimental "lab" for vector fusion and similarity math.
*   `/src`: The core recommendation engine (`engine.py`).

Note: I cleared the output of the first 2 notebooks so I don’t leak my IDs or the raw RapidAPI data. For the rest, I left the outputs in place so you can see the analysis and results.

---

*Created by an aspiring Data Scientist who spends way too much time thinking about game aesthetics. This project explores API integration and the use of math to model the subjective beauty of music.*