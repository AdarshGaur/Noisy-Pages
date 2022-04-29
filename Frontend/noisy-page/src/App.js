import './App.css';
import Navbar from "./Navbar/Navbar.js"
import BlogCards from "./BlogPost/BlogCard.js"
import Sidebar from "./Sidebar/Sidebar.js"
import Footer from "./Footer./Footer.js"

function App() {
  return (
    <div className="App">
      <Navbar />
      <BlogCards />
      <Sidebar />
      <Footer />
    </div>
  );
}

export default App;
