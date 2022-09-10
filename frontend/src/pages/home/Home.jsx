import axios from "axios";
import { useEffect, useState } from "react";
import { useLocation } from "react-router";
import Header from "../../header/Header"
import Posts from "../../posts/Posts"
import Sidebar from "../../sidebar/Sidebar"
import "./home.css"


export default function Home(){
	const [posts, setPosts] = useState([]);
	const { search } = useLocation();
	
	useEffect(() => {
		const fetchPosts = async () => {
			const res = await axios.get("/posts" + search);
			setPosts(res.data);
		}
		fetchPosts();
	}, [search]);
	
	return(
		<>
		<Header/>
		<div className="home">
			<Posts posts={posts}/>
			<Sidebar />
		</div>
		</>
	)
}