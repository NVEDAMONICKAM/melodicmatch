import { motion, useMotionValue, useTransform } from "framer-motion";
import { useState } from "react";

interface Props {
	track: any;
	onSwipe: (liked: boolean) => void;
}

export default function SwipeCard({ track, onSwipe }: Props) {
	const x = useMotionValue(0);

	const rotate = useTransform(x, [-200, 200], [-15, 15]);
	const opacity = useTransform(x, [-200, 0, 200], [0.5, 1, 0.5]);

	return (
		<motion.div
			drag="x"
			style={{ x, rotate, opacity }}
			dragConstraints={{ left: 0, right: 0 }}
			onDragEnd={(_, info) => {
				if (info.offset.x > 120) {
					onSwipe(true);
				} else if (info.offset.x < -120) {
					onSwipe(false);
				}
			}}
			className="card"
		>
			<img
				src={track.album_cover_url}
				className="cover"
				alt={track.track_name}
			/>
			<div className="card-content">
				<h2>{track.track_name}</h2>
				<p>{track.artist}</p>
			</div>
		</motion.div>
	);
}