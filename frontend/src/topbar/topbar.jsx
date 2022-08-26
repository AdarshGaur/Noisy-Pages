import React from "react"
import "./topbar.css"
import logo from "../assets/logo.png"

export default function Topbar(){
	return(
		<div className="top">
			<div className="topRight">
				<img
					className="topImage"
					src = {logo}
					alt="logo" 
				/>
				<i class="topSearchIcon fa-solid fa-magnifying-glass"></i>
			</div>
			<div className="topCenter">
				<ul className="topList">
					<li className="topListItem">HOME</li>
					<li className="topListItem">ABOUT</li>
					<li className="topListItem">CONTACT</li>
					<li className="topListItem">WRITE</li>
					<li className="topListItem">LOGOUT</li>
				</ul>
			</div>
			<div className="topLeft">
				<i className="topIcon fa-brands fa-instagram"></i>
				<i className="topIcon fa-brands fa-facebook-f"></i>
				<i className="topIcon fa-brands fa-twitter"></i>
				<i className="topIcon fa-brands fa-pinterest-p"></i>
			</div>
		</div>
	)
}