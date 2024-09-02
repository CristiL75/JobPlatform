import React, { useState, useEffect } from 'react';
import axios from 'axios';
import JobSeekerPostForm from './JobSeekerPostForm';
import '../styles/JobSeekerPosts.css';

function JobSeekerPosts() {
  const [jobSeekerPosts, setJobSeekerPosts] = useState([]);
  const [filteredPosts, setFilteredPosts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedPostId, setExpandedPostId] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingPostId, setEditingPostId] = useState(null);
  const [username, setUsername] = useState(null);
  const [formData, setFormData] = useState(null);

  // Fetch username from localStorage
  const fetchUsername = () => {
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    } else {
      console.error('Username not found in localStorage');
    }
  };

  useEffect(() => {
    fetchUsername();
    fetchJobSeekerPosts();
  }, []);

  const fetchJobSeekerPosts = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://localhost:8000/api/job-seeker-posts/');
      console.log('API Response:', response.data);
      if (Array.isArray(response.data)) {
        setJobSeekerPosts(response.data);
        setFilteredPosts(response.data);
      } else {
        setError('Unexpected response format.');
      }
    } catch (error) {
      setError('Failed to load job seeker posts.');
      console.error('Error fetching posts:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (searchTerm === '') {
      setFilteredPosts(jobSeekerPosts);
    } else {
      const filtered = jobSeekerPosts.filter(post =>
        post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.skills.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.industry.toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredPosts(filtered);
    }
  }, [searchTerm, jobSeekerPosts]);

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handlePostSubmit = async (postData) => {
    try {
      if (!username) {
        throw new Error('Username is not available');
      }

      const postDataWithUsername = {
        ...postData,
        created_by: username,
      };

      console.log('Submitting post data:', postDataWithUsername);

      if (editingPostId) {
        const response = await axios.put(`http://localhost:8000/api/job-seeker-posts/${editingPostId}/`, postDataWithUsername, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.status === 200) {
          console.log('Post updated successfully');
          setEditingPostId(null);
          fetchJobSeekerPosts();
        } else {
          console.error('Unexpected response:', response);
        }
      } else {
        const response = await axios.post('http://localhost:8000/api/job-seeker-posts/', postDataWithUsername, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (response.status === 201) {
          console.log('Post created successfully');
          fetchJobSeekerPosts();
        } else {
          console.error('Unexpected response:', response);
        }
      }

      setShowForm(false);
    } catch (error) {
      console.error('Error submitting post:', error);
      if (error.response) {
        console.error('Error response data:', error.response.data);
      }
    }
  };

  const handleEditClick = (post) => {
    setEditingPostId(post.id);
    setFormData(post);
    setShowForm(true);
  };

  const handleDeletePost = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/job-seeker-posts/${id}/`);
      console.log('Post deleted successfully');
      fetchJobSeekerPosts();
    } catch (error) {
      console.error('Error deleting post:', error);
      if (error.response) {
        console.error('Error response data:', error.response.data);
      }
    }
  };

  const handlePostClick = (id) => {
    setExpandedPostId(expandedPostId === id ? null : id); // Toggle expand/collapse
  };

  const handleUsernameClick = (username) => {
    window.location.href = `/profile/${username}`;
  };

  const toggleFormVisibility = () => {
    setShowForm(!showForm);
    if (!showForm) {
      setEditingPostId(null);
      setFormData(null);
    }
  };

  return (
    <div className="job-seeker-posts">
      <h1>Job Seeker Posts</h1>

      {/* Toggle button for showing the form */}
      <button className="toggle-form-button" onClick={toggleFormVisibility}>
        {showForm ? 'Cancel' : (editingPostId ? 'Update Job Post' : 'Create Job Post')}
      </button>

      {/* Conditionally render the form */}
      {showForm && <JobSeekerPostForm onSubmit={handlePostSubmit} initialData={formData} />}

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search posts..."
        value={searchTerm}
        onChange={handleSearchChange}
        className="search-bar"
      />

      {loading && <p>Loading...</p>}
      {error && <p className="error-message">{error}</p>}

      {/* Conditional rendering based on the posts length */}
      {filteredPosts.length === 0 && !loading && !error && (
        <p>No job seeker posts available.</p>
      )}

      {Array.isArray(filteredPosts) && (
        <div className="posts-container">
          {filteredPosts.map(post => (
            <div
              className={`post-card ${expandedPostId === post.id ? 'expanded' : ''}`}
              key={post.id}
              onClick={() => handlePostClick(post.id)}
            >
              <h2>{post.title}</h2>
              <p>
                <strong>Description:</strong> {expandedPostId === post.id ? post.description : post.description.slice(0, 100) + '...'}
              </p>
              <p><strong>Skills:</strong> {post.skills}</p>
              <p><strong>Experience Level:</strong> {post.experience_level}</p>
              <p><strong>Preferred Location:</strong> {post.preferred_location}</p>
              <p><strong>Employment Type:</strong> {post.employment_type}</p>
              <p><strong>Industry:</strong> {post.industry}</p>
              <p>
                <strong>Posted by:</strong> 
                <span
                  className="username-link"
                  onClick={() => handleUsernameClick(post.created_by)}
                >
                  {post.created_by}
                </span>
              </p>
              {expandedPostId === post.id && (
                <div className="post-details">
                  <p><strong>Created At:</strong> {new Date(post.created_at).toLocaleDateString()}</p>
                  {username === post.created_by && (
                    <div>
                      <button onClick={() => handleEditClick(post)}>Edit</button>
                      <button onClick={() => handleDeletePost(post.id)}>Delete</button>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default JobSeekerPosts;
