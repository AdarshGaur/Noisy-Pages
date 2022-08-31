import "./singlePost.css"

export default function SinglePost() {
	return (
		<div className="singlePost">
			<div className="singlePostWrapper">
				<img 
					src="" 
					alt="" 
					className="singlePostImg"
				/>
				<h1 className="singlePostTitle">
					Lorem ipsum dolor sit amet consectetur.
					<div className="singlePostEdit">
						<i className="singlePostIcon far fa-edit"></i>
						<i className="singlePostIcon far fa-trash-alt"></i>
					</div>
				</h1>
				<div className="singlePostInfo">
					<span className="singlePostAuthor">Author: <b> Name </b></span>
					<span className="singlePostDate"> x hrs ago </span>
				</div>
				<p className="singlePostDesc">
					Content, Lorem ipsum dolor sit amet consectetur adipisicing elit. Nam doloribus voluptates, omnis sapiente tempore at earum pariatur illum. Minus, obcaecati voluptate aperiam quos illo nesciunt iure minima nemo repellendus expedita.
				</p>
			</div>
		</div>
	);
}