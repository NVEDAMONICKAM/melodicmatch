import axios from "axios";

const API = axios.create({
	baseURL: "http://127.0.0.1:8000",
});

export const getNextTrack = async () => {
	const res = await API.get("/next-track");
	return res.data;
};

export const swipeTrack = async (
	user_id: string,
	track_id: string,
	liked: boolean
) => {
	await API.post("/swipe", {
		user_id,
		track_id,
		liked,
	});
};

export const getRecommendations = async (user_id: string) => {
	const res = await API.get("/recommend", {
		params: { user_id, k: 5 },
	});
	return res.data;
};