import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Home() {
  const [username, setUsername] = useState(""); // Initial state for username
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    // Fetch username from localStorage when component mounts
    const storedUsername = localStorage.getItem("username");
    console.log("Stored Username:", storedUsername); // Debug line
    if (storedUsername) {
      setUsername(storedUsername);
    }
  }, []);

  const handleProfileClick = () => {
    // Redirect user to their profile page
    navigate(`/profile/${username}`);
  };

  const handleJobPostsClick = () => {
    // Redirect user to the job posts page
    navigate("/job-posts");
  };

  const handleJobSeekerPostsClick = () => {
    // Redirect user to the job seeker posts page
    navigate("/job-seeker-posts");
  };

  return (
    <div>
      {/* Navbar */}
      <nav style={navbarStyle}>
        <div style={navbarContentStyle}>
          {/* Display username or "Guest" if no username is found */}
          <span style={usernameStyle} onClick={handleProfileClick}>
            {username || "Guest"}
          </span>
          {/* Link to Job Posts page */}
          <span style={navLinkStyle} onClick={handleJobPostsClick}>
            Joburi
          </span>
          {/* Link to Job Seeker Posts page */}
          <span style={navLinkStyle} onClick={handleJobSeekerPostsClick}>
          job listings
          </span>
        </div>
      </nav>

      {/* Home page content */}
      <div>
        <h1>Welcome to the Home Page!</h1>
        {/* Add additional content here */}
      </div>
    </div>
  );
}

// Simple styling for the navbar
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
