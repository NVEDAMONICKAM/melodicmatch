import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class TrackRecommender:
    def __init__(self, feature_path="data/features.parquet",
                 metadata_path="data/processed/silver_tracks.parquet",
                 min_swipes=5):

        # Load features
        self.feature_df = pd.read_parquet(feature_path, engine="pyarrow")
        self.track_ids = self.feature_df["track_id"].tolist()

        # ID → index map (O(1) lookup)
        self.id_to_index = {
            track_id: idx for idx, track_id in enumerate(self.track_ids)
        }

        # Convert vector column
        self.track_matrix = np.vstack(
            self.feature_df["features"].apply(lambda v: v["values"]).values
        )

        self.feature_dim = self.track_matrix.shape[1]

        # Load metadata
        self.metadata_df = pd.read_parquet(metadata_path, engine="pyarrow")
        self.metadata_df = self.metadata_df.set_index("track_id")

        # User state
        self.user_vector = np.zeros(self.feature_dim)
        self.swiped_tracks = set()
        self.swipe_count = 0
        self.min_swipes = min_swipes

    def swipe(self, track_id: str, liked: bool):
        if track_id not in self.id_to_index:
            return

        idx = self.id_to_index[track_id]
        track_vector = self.track_matrix[idx]

        if liked:
            self.user_vector += track_vector
        else:
            self.user_vector -= track_vector

        self.swiped_tracks.add(track_id)
        self.swipe_count += 1

    def _compute_similarities(self):
        norm = np.linalg.norm(self.user_vector)
        if norm == 0:
            return None

        normalized_user = self.user_vector / norm
        similarities = cosine_similarity(
            [normalized_user],
            self.track_matrix
        )[0]

        return similarities

    def recommend_top_k(self, k=5):
        if self.swipe_count < self.min_swipes:
            return {
                "error": f"Minimum {self.min_swipes} swipes required",
                "current_swipes": self.swipe_count
            }

        similarities = self._compute_similarities()
        if similarities is None:
            return None

        ranked_indices = np.argsort(similarities)[::-1]

        recommendations = []

        for idx in ranked_indices:
            track_id = self.track_ids[idx]

            if track_id in self.swiped_tracks:
                continue

            metadata = self.metadata_df.loc[track_id]

            recommendations.append({
                "track_id": track_id,
                "track_name": metadata["track_name"],
                "artist": metadata["primary_artist_name"],
                "album_cover_url": metadata["album_cover_url"],
                "similarity_score": float(similarities[idx])
            })

            if len(recommendations) == k:
                break

        return recommendations