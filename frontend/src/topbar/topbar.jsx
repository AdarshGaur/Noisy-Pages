import React from "react"
import "./topbar.css"
import logo from "../assets/logo.png"
import { Link } from "react-router-dom"

export default function Topbar(){
	const currentUser = false
	return(
		<div className="top">
			<div className="topLeft">
				<i className="topIcon fa-brands fa-instagram"></i>
				<i className="topIcon fa-brands fa-facebook-f"></i>
				<i className="topIcon fa-brands fa-twitter"></i>
				<i className="topIcon fa-brands fa-pinterest-p"></i>
			</div>
			<div className="topCenter">
				<ul className="topList">
					<li className="topListItem">
						<Link className="link" to="/">HOME</Link>
					</li>
					<li className="topListItem">
						<Link className="link" to="/">ABOUT</Link>
					</li>
					<li className="topListItem">
						<Link className="link" to="/">CONTACT</Link>
					</li>
					<li className="topListItem">
						<Link className="link" to="/write">WRITE</Link>
					</li>
					<li className="topListItem">
						{currentUser && "LOGOUT"}
					</li>
				</ul>
			</div>
			<div className="topRight">
				{currentUser ? (
					<Link className="link" to="/settings">
					<img
						className="topImage"
						src = {logo}
						alt="logo" 
					/>
					</Link>
					) : (
						<ul className="topList">
							<li className="topListItem">
								<Link className="link" to="/login">
									SIGN IN
								</Link>
							</li>
							<li className="topListItem">
								<Link className="link" to="/register">
									SIGN UP
								</Link>
							</li>
						</ul>
					)
				}
				<i class="topSearchIcon fa-solid fa-magnifying-glass"></i>
			</div>
		</div>
	)
}