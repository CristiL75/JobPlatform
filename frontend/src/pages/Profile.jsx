import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api'; // Import API configuration
import { ACCESS_TOKEN } from '../constants'; // Import constants
import '../styles/Profile.css'; // Import styles

function Profile() {
  const { username: profileUsername } = useParams(); // Retrieve the username from the URL
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({
    city: '',
    education: '',
    experience: '',
    skills: '',
    certifications: '',
    languages: '',
    interests: '',
    resume: null
  });
  const [loading, setLoading] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [isOwner, setIsOwner] = useState(false); // State to check if the user is the profile owner
  const navigate = useNavigate(); // Hook for navigation

  // Fetch profile data
  const fetchProfile = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      const response = await api.get(`/api/user/profile/${profileUsername}/`, { // Updated endpoint to include username
        headers: { Authorization: `Bearer ${token}` },
      });
      setProfile(response.data);

      // Check if the current user is the owner of the profile
      const currentUsername = localStorage.getItem('username');
      setIsOwner(response.data.username === currentUsername);

      setFormData({
        city: response.data.city || '',
        education: response.data.education || '',
        experience: response.data.experience || '',
        skills: response.data.skills || '',
        certifications: response.data.certifications || '',
        languages: response.data.languages || '',
        interests: response.data.interests || '',
        resume: response.data.resume || null
      });
    } catch (error) {
      console.error('Error fetching profile:', error);
      alert('Failed to load profile.');
      navigate('/'); // Redirect to home if the profile fetch fails
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, [profileUsername]);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setFormData({ ...formData, [id]: value });
  };

  const handleFileChange = (e) => {
    setFormData({ ...formData, resume: e.target.files[0] });
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setLoading(true);

    const data = new FormData();
    Object.keys(formData).forEach(key => {
      if (formData[key]) {
        data.append(key, formData[key]);
      }
    });

    try {
      const token = localStorage.getItem(ACCESS_TOKEN);
      await api.post(`/api/user/profile/${profileUsername}/`, data, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Profile updated successfully!');
      setEditMode(false);
      fetchProfile();  // Refresh profile data after update
    } catch (error) {
      console.error('Error updating profile:', error);
      alert('Failed to update profile.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-container">
      <h1>{editMode ? 'Edit Profile' : 'View Profile'}</h1>
      {loading && <p>Loading...</p>}
      {!loading && profile && !editMode && (
        <div className="profile-view">
          <p><strong>City:</strong> {profile.city}</p>
          <p><strong>Education:</strong> {profile.education}</p>
          <p><strong>Experience:</strong> {profile.experience}</p>
          <p><strong>Skills:</strong> {profile.skills}</p>
          <p><strong>Certifications:</strong> {profile.certifications}</p>
          <p><strong>Languages:</strong> {profile.languages}</p>
          <p><strong>Interests:</strong> {profile.interests}</p>
          <p><strong>Resume:</strong> {profile.resume ? <a href={`http://localhost:8000${profile.resume}`} target="_blank" rel="noopener noreferrer">View Resume</a> : 'No resume uploaded'}</p>
          {isOwner && <button onClick={() => setEditMode(true)}>Edit Profile</button>}
        </div>
      )}
      {editMode && isOwner && (
        <form onSubmit={handleUpdateProfile} className="profile-form">
          <div>
            <label htmlFor="city">City</label>
            <input
              type="text"
              id="city"
              value={formData.city}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="education">Education</label>
            <textarea
              id="education"
              value={formData.education}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="experience">Experience</label>
            <textarea
              id="experience"
              value={formData.experience}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="skills">Skills</label>
            <textarea
              id="skills"
              value={formData.skills}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="certifications">Certifications</label>
            <textarea
              id="certifications"
              value={formData.certifications}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="languages">Languages</label>
            <textarea
              id="languages"
              value={formData.languages}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="interests">Interests</label>
            <textarea
              id="interests"
              value={formData.interests}
              onChange={handleInputChange}
            />
          </div>
          <div>
            <label htmlFor="resume">Resume (PDF)</label>
            <input
              type="file"
              id="resume"
              accept=".pdf"
              onChange={handleFileChange}
            />
          </div>
          <button type="submit" disabled={loading}>Save Changes</button>
          <button type="button" onClick={() => setEditMode(false)}>Cancel</button>
        </form>
      )}
      {!isOwner && <p>You do not have permission to edit this profile.</p>}
    </div>
  );
}

export default Profile;
