import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Students from "./pages/Students";

function Dashboard() {
	return (
		<div style={{ padding: 20 }}>
			<h2>Dashboard (MVP)</h2>
			<p>Welcome — basic MVP interface.</p>
		</div>
	);
}

export default function App() {
	return (
		<div>
			<header style={{ padding: "8px 16px", borderBottom: "1px solid #ddd" }}>
				<Link to="/">Home</Link> | <Link to="/students">Students</Link>
			</header>
			<main>
				<Routes>
					<Route path="/" element={<Dashboard />} />
					<Route path="/students" element={<Students />} />
				</Routes>
			</main>
		</div>
	);
}
