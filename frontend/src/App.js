import Topbar from "./topbar/topbar";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/home/Home";
import Register from "./pages/registser/Register";
import Login from "./pages/login/Login";
import Settings from "./pages/settings/Settings";
import Write from "./pages/write/Write";
import Single from "./pages/single/Single";


function App() {
	const user = false
	return (
		<Router>
			<Topbar />
			<Routes>
				<Route path='/' element={<Home />} />
				<Route path="/posts" element={<Home />} />
				<Route path="/register" element={currentUser ? <Home /> : <Register/>} />
				<Route path="/login" element={currentUser ? <Home /> : <Login/>} />
				<Route path="/post/:id" element={<Single />} />
				<Route path="/write" element={currentUser ? <Write /> : <Login />} />
				<Route path="/settings" element={currentUser ? <Settings /> : <Login />} />
				<Route path="/post/:postId">
					<Single />
				</Route>
			</Routes>
		</Router>
	);
}

export default App;
