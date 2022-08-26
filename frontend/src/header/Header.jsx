import "./header.css"
// import hImage from "../assets/home1.jpg"

export default function Header(){
	return(
		<div className="header">
			<div className="headerTitles">
				<span className="headerTitleSm">Noisy Pages</span>
				<span className="headerTitleLg">BLOGS</span>
			</div>
			<img
				className="headerImg"
				src="https://images.pexels.com/photos/1167355/pexels-photo-1167355.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
				alt="Asthetics"
			/>
		</div>
	)
}