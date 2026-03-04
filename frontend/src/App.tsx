import { useEffect, useState } from "react";
import SwipeCard from "./components/SwipeCard";
import { getNextTrack, getRecommendations, swipeTrack } from "./api";

const USER_ID = "demo_user";

function Recommendation({ rec, onContinue }: any) {
  return (
    <div className="card">
      <h2>Recommended For You</h2>

      <img src={rec.album_cover_url} className="cover" />

      <h3>{rec.track_name}</h3>
      <p>{rec.artist}</p>

      <div className="buttons">
        <button className="btn primary">
          Listen Now
        </button>

        <button className="btn secondary" onClick={onContinue}>
          Keep Swiping
        </button>
      </div>
    </div>
  );
}

export default function App() {
  const [track, setTrack] = useState<any>(null);
  const [swipeCount, setSwipeCount] = useState(0);
  const [recommendation, setRecommendation] = useState<any>(null);

  const loadNext = async () => {
    const data = await getNextTrack();
    setTrack(data);
  };

  useEffect(() => {
    loadNext();
  }, []);

  const handleSwipe = async (liked: boolean) => {
    if (!track) return;

    await swipeTrack(USER_ID, track.track_id, liked);

    const newCount = swipeCount + 1;
    setSwipeCount(newCount);

    if (newCount >= 10) {
      const recs = await getRecommendations(USER_ID);
      setRecommendation(recs[0]); // take best recommendation
    } else {
      loadNext();
    }
  };

  return (
    <div className="app">
      <h1 className="title">MelodicMatch</h1>

      {recommendation ? (
        <Recommendation
          rec={recommendation}
          onContinue={() => {
            setRecommendation(null);
            setSwipeCount(0);
            loadNext();
          }}
        />
      ) : (
        track && <SwipeCard track={track} onSwipe={handleSwipe} />
      )}

      <div className="buttons">
        <button className="btn secondary" onClick={() => handleSwipe(false)}>
          Skip
        </button>
        <button className="btn primary" onClick={() => handleSwipe(true)}>
          Like
        </button>
      </div>
    </div>
  );
}