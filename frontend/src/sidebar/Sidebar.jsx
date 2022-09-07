import axios from "axios";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./sidebar.css"

export default function Sidebar(){
	const [cats, setCats] = useState([]);
	
	useEffect( () => {
		const getCats = async() => {
			const res = await axios. get("/categories");
			setCats(res.data);
		};
		getCats();
	}, []);
	
	
	
	return (
		<div className="sidebar">
			<div className="sidebarItem">
				<span className="sidebarTitle">ABOUT ME</span>
				<img
					src="https://i.pinimg.com/236x/1e/3f/58/1e3f587572a7a7b20bbf1828595a1786--holiday-party-themes-holiday-gift-guide.jpg"
					alt="Profile"
				/>
				<p>
				Laboris sunt aute cupidatat velit magna velit ullamco dolore mollit
				amet ex esse.Sunt eu ut nostrud id quis proident.
				</p>
			</div>
			<div className="sidebarItem">
				<span className="sidebarTitle">CATEGORIES</span>
				<ul className="sidebarList">
					{cats.map((c) => (
						<Link to={`/?cat=${c.name}`} className="link">
							<li className="sidebarListItem">{c.name}</li>
						</Link>
					))}
				</ul>
			</div>
			<div className="sidebarItem">
				<span className="sidebarTitle">FOLLOW US</span>
				<div className="sidebarSocial">
					<i className="sidebarIcon fa-brands fa-instagram"></i>
					<i className="sidebarIcon fa-brands fa-facebook-f"></i>
					<i className="sidebarIcon fa-brands fa-twitter"></i>
					<i className="sidebarIcon fa-brands fa-pinterest-p"></i>
				</div>
			</div>
		</div>
	)
}