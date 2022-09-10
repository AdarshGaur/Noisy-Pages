import "./header.css"
import headerimage from "../assets/headerImage.jpg"

export default function Header(){
	return(
		<div className="header">
			<div className="headerTitles">
				<span className="headerTitleSm">BlogSite</span>
				<span className="headerTitleLg">Noisy Pages</span>
			</div>
			<img
				className="headerImg"
				src={headerimage}
				alt="Asthetics"
			/>
		</div>
	)
}