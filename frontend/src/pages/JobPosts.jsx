import { useState, useEffect } from 'react';
import axios from 'axios';
import api from '../api';
import '../styles/JobPosts.css';
import { ACCESS_TOKEN } from '../constants'; 
import { Link } from 'react-router-dom';

function JobPosts() {
  const [jobPosts, setJobPosts] = useState([]);
  const [filteredJobPosts, setFilteredJobPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [creating, setCreating] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    location: '',
    company: '',
    salary: '',
    employment_type: '',
    domain: '',
    experience_level: '',
    job_type: '',
    languages: '',
    skills: '',
  });
  const [editingJob, setEditingJob] = useState(null);
  const [currentUsername, setCurrentUsername] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [interests, setInterests] = useState(new Set());
  const [interestedUsers, setInterestedUsers] = useState([]);

  // Fetch job posts from the API
  const fetchJobPosts = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/api/job-posts/');
      setJobPosts(response.data || []);
    } catch (error) {
      setError('Failed to load job posts.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch users interested in a specific job post
  const fetchInterests = async (jobPostId) => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const response = await axios.get(`http://127.0.0.1:8000/api/job-posts/${jobPostId}/interested/users/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setInterestedUsers(response.data);
    } catch (error) {
      console.error('Failed to fetch interests:', error);
    }
  };

  // Fetch job posts and username on component mount
  useEffect(() => {
    const username = localStorage.getItem('username');
    setCurrentUsername(username);
    fetchJobPosts();
  }, []);

  // Update filtered job posts based on search term
  useEffect(() => {
    const term = searchTerm.toLowerCase().trim();
    if (term === '') {
      setFilteredJobPosts(jobPosts);
    } else {
      setFilteredJobPosts(
        jobPosts.filter((job) =>
          Object.values(job).some(value =>
            value.toString().toLowerCase().includes(term)
          )
        )
      );
    }
  }, [searchTerm, jobPosts]);

  // Handle form input changes
  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewJob(prevNewJob => ({ ...prevNewJob, [name]: value }));
  };

  // Handle search input changes
  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  // Handle create or update job post
  const handleCreateOrUpdateJobPost = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (editingJob) {
        await api.put(`/api/job-posts/${editingJob.id}/`, newJob);
      } else {
        await api.post('/api/job-posts/', newJob);
      }
      await fetchJobPosts();
      resetJobForm();
    } catch (error) {
      setError('Failed to create or update job post.');
    } finally {
      setLoading(false);
    }
  };

  // Handle delete job post
  const handleDeleteJobPost = async (jobId) => {
    setLoading(true);
    setError(null);
    try {
      await api.delete(`/api/job-posts/${jobId}/`);
      await fetchJobPosts();
    } catch (error) {
      setError('Failed to delete job post.');
    } finally {
      setLoading(false);
    }
  };

  // Handle show interest in a job post
  const handleShowInterest = async (jobId) => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      if (!token) {
        throw new Error('No authentication token found');
      }

      await axios.post(
        `http://127.0.0.1:8000/api/job-posts/${jobId}/interest/`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setInterests(prevInterests => new Set(prevInterests).add(jobId));
    } catch (error) {
      console.error('Failed to show interest:', error.response ? error.response.data : error.message);
      setError('Failed to show interest. Please check your authentication and try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle username button click
  const handleUsernameClick = (username) => {
    window.location.href = `/profile/${username}`;
  };

  // Reset job form
  const resetJobForm = () => {
    setCreating(false);
    setEditingJob(null);
    setNewJob({
      title: '',
      description: '',
      location: '',
      company: '',
      salary: '',
      employment_type: '',
      domain: '',
      experience_level: '',
      job_type: '',
      languages: '',
      skills: '',
    });
  };

  return (
    <div className="job-posts-container">
      <h1>Job Posts</h1>
      <input
        type="text"
        placeholder="Search job posts..."
        value={searchTerm}
        onChange={handleSearchChange}
        className="search-input"
      />

      <button onClick={() => setCreating(!creating)}>
        {creating ? 'Cancel' : (editingJob ? 'Cancel Editing' : 'Create New Job Post')}
      </button>

      {(creating || editingJob) && (
        <form onSubmit={handleCreateOrUpdateJobPost} className="create-job-form">
          {Object.keys(newJob).map((key) => (
            <div key={key}>
              <label htmlFor={key}>{key.replace(/_/g, ' ')}</label>
              {key === 'description' ? (
                <textarea
                  id={key}
                  name={key}
                  value={newJob[key]}
                  onChange={handleInputChange}
                  required
                />
              ) : (
                <input
                  type="text"
                  id={key}
                  name={key}
                  value={newJob[key]}
                  onChange={handleInputChange}
                  required={['title', 'location', 'company'].includes(key)}
                />
              )}
            </div>
          ))}
          <button type="submit" disabled={loading}>
            {editingJob ? 'Update' : 'Submit'}
          </button>
        </form>
      )}

      {error && <div style={{ color: 'red' }}>{error}</div>}
      {loading && <div>Loading...</div>}
      {!loading && filteredJobPosts.length > 0 ? (
        <ul className="job-posts-list">
          {filteredJobPosts.map((job) => (
            <li key={job.id}>
              <h2>{job.title}</h2>
              <div><strong>Description:</strong> {job.description}</div>
              <div><strong>Location:</strong> {job.location}</div>
              <div><strong>Company:</strong> {job.company}</div>
              <div><strong>Salary:</strong> {job.salary}</div>
              <div><strong>Employment Type:</strong> {job.employment_type}</div>
              <div><strong>Domain:</strong> {job.domain}</div>
              <div><strong>Experience Level:</strong> {job.experience_level}</div>
              <div><strong>Job Type:</strong> {job.job_type}</div>
              <div><strong>Languages:</strong> {job.languages}</div>
              <div><strong>Skills:</strong> {job.skills}</div>
              <div><strong>Created At:</strong> {new Date(job.created_at).toLocaleString()}</div>
              <div>
                <strong>Created By:</strong>
                {job.created_by ? (
                  <>
                    <button onClick={() => handleUsernameClick(job.created_by.username)}>
                      {job.created_by.username}
                    </button>
                    {job.created_by.username === currentUsername ? (
                      <>
                        <button onClick={() => {
                          setEditingJob(job);
                          setNewJob({
                            title: job.title,
                            description: job.description,
                            location: job.location,
                            company: job.company,
                            salary: job.salary,
                            employment_type: job.employment_type,
                            domain: job.domain,
                            experience_level: job.experience_level,
                            job_type: job.job_type,
                            languages: job.languages,
                            skills: job.skills,
                          });
                          setCreating(true);
                        }}>
                          Edit
                        </button>
                        <button onClick={() => handleDeleteJobPost(job.id)}>
                          Delete
                        </button>
                        {/* Section to show interested users */}
                        <button onClick={() => fetchInterests(job.id)}>
                          View Interested Users
                        </button>
                        {interestedUsers.length > 0 && (
                          <ul>
                          {interestedUsers.length > 0 && (
  <ul>
    {interestedUsers.map(user => (
      <li key={user.user}>
        <Link to={`/profile/${user.user}`}>
          {user.user}
        </Link>
      </li>
    ))}
  </ul>
)}
                          </ul>
                        )}
                      </>
                    ) : (
                      !interests.has(job.id) && (
                        <button onClick={() => handleShowInterest(job.id)}>
                          Show Interest
                        </button>
                      )
                    )}
                  </>
                ) : (
                  'Unknown'
                )}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        !loading && <div>No job posts available.</div>
      )}
    </div>
  );
}

export default JobPosts;
