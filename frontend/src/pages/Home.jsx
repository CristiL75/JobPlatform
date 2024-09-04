import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Chatbot from './Chatbot'; 

function Home() {
  const [username, setUsername] = useState(""); 
  const navigate = useNavigate(); 



  useEffect(() => {
    const storedUsername = localStorage.getItem("username");
    console.log("Stored Username:", storedUsername); 
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const handleProfileClick = () => {
    navigate(`/profile/${username}`);
  };

  const handleJobPostsClick = () => {
    navigate("/job-posts");
  };

  const handleJobSeekerPostsClick = () => {
    navigate("/job-seeker-posts");
  };

  return (
    <div>
      {/* Navbar */}
      <nav style={navbarStyle}>
        <div style={navbarContentStyle}>
          <span style={usernameStyle} onClick={handleProfileClick}>
            {username || "Guest"}
          </span>
          <span style={navLinkStyle} onClick={handleJobPostsClick}>
            Joburi
          </span>
          <span style={navLinkStyle} onClick={handleJobSeekerPostsClick}>
            job listings
          </span>
        </div>
      </nav>

      {/* Home page content */}
      <div>
        <h1>Welcome to the Home Page!</h1>
        {/* Include the Chatbot component */}
        <Chatbot />
      </div>
    </div>
  );
}

const navbarStyle = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  backgroundColor: "#333",
  padding: "10px 20px",
};

const navbarContentStyle = {
  display: "flex",
  alignItems: "center",
};

const usernameStyle = {
  color: "#fff",
  cursor: "pointer",
  fontSize: "18px",
  marginRight: "20px",
};

const navLinkStyle = {
  color: "#fff",
  cursor: "pointer",
  fontSize: "18px",
  marginRight: "20px",
};

export default Home;
