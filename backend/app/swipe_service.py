from app.recommender import TrackRecommender

recommender = TrackRecommender()


def handle_swipe(track_id: str, liked: bool):
    recommender.swipe(track_id, liked)


def get_top_recommendations(k=5):
    return recommender.recommend_top_k(k)


def get_next_track():
    for track_id in recommender.track_ids:
        if track_id not in recommender.swiped_tracks:
            metadata = recommender.metadata_df.loc[track_id]
            return {
                "track_id": track_id,
                "track_name": metadata["track_name"],
                "artist": metadata["primary_artist_name"],
                "album_cover_url": metadata["album_cover_url"]
            }

    return None