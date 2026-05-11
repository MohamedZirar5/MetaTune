# 🎧 MetaTune: The Beat of Your Gameplay

**MetaTune** is a Data Science project born from my love for video game original soundtracks (OSTs). After finishing a game or spending hours in its world, I often listen to the OST on loop.

This project answers the question:
**"How can I find songs that match the vibe of a specific game or, even better, a blend of multiple games I'm playing?"**

While many users create these playlists manually, they are often biased toward individual taste. As an incoming Data Science Master's student and long-time gamer, I wanted to build an automated music recommender that bridges the gap between gaming and music through data.

## The Core Idea: Multi-Atmosphere Fusion
Most recommenders analyze one source at a time. **MetaTune** allows you to blend multiple games that currently matches your mood. We'll call those "meta-moods"

Want the epic, orchestral scale of *The Legend of Zelda* mixed with the gritty, industrial anxiety of *Lethal Company*? The engine calculates a **Mood Centroid**—a mathematical "sweet spot" between these worlds—to find tracks that sit at the intersection of your favorite games.

## Project Roadmap
- [ ] *Phase 1:* Leveraging the `Spotipy` API to extract high-dimensional audio features (Energy, Valence, Acousticness, etc.) from game OSTs.
- [ ] *Phase 2:* Building a vector-based aggregator that merges multiple game profiles into a single "target vibe" using weighted averages.
- [ ] *Phase 3:* Implementing `MinMaxScaler` for data normalization and using Euclidean Distance to rank the tracks that are "closest" to the game's atmosphere.
- [ ] **Phase 4:* Creating interactive Radar Charts to visualize how well a recommended song overlaps with the game's profile.

## Tech Stack
*   **Data Science:** Pandas & NumPy
*   **Machine Learning:** Scikit-Learn (`MinMaxScaler`, Similarity Metrics)
*   **APIs:** Spotipy (Spotify Web API)
*   **Visuals:** Plotly / Matplotlib

## Structure
*   `/data`: The "Sound Signatures"—curated datasets of audio features.
*   `/notebooks`: Experimental "lab" for vector fusion and similarity math.
*   `/src`: The core recommendation engine (`engine.py`).

---

*Created by an aspiring Data Scientist who spends way too much time thinking about game aesthetics. This project explores API integration and the use of math to model the subjective beauty of music.*