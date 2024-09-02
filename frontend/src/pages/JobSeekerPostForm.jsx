import React, { useState, useEffect } from 'react';
import '../styles/JobSeekerPostForm.css';
import PropTypes from 'prop-types'; // Optional: add PropTypes if needed

function JobSeekerPostForm({ onSubmit, initialData = {} }) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    skills: '',
    experienceLevel: '',
    preferredLocation: '',
    employmentType: '',
    industry: '',
  });

  // Initialize form with initial data when it is provided
  useEffect(() => {
    if (initialData) {
      setFormData({
        title: initialData.title || '',
        description: initialData.description || '',
        skills: initialData.skills || '',
        experienceLevel: initialData.experience_level || '',
        preferredLocation: initialData.preferred_location || '',
        employmentType: initialData.employment_type || '',
        industry: initialData.industry || '',
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (onSubmit) {
      const formattedData = {
        title: formData.title,
        description: formData.description,
        skills: formData.skills.slice(0, 500), // Truncate if necessary
        experience_level: formData.experienceLevel,
        preferred_location: formData.preferredLocation,
        employment_type: formData.employmentType,
        industry: formData.industry,
      };
      onSubmit(formattedData); // Call the onSubmit prop function with formatted data
    }
    // Optionally, reset the form fields after submission, if needed
    // setFormData({
    //   title: '',
    //   description: '',
    //   skills: '',
    //   experienceLevel: '',
    //   preferredLocation: '',
    //   employmentType: '',
    //   industry: '',
    // });
  };

  return (
    <form onSubmit={handleSubmit} className="job-seeker-post-form">
      <div className="form-group">
        <label htmlFor="title">Job Title:</label>
        <input
          type="text"
          id="title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>

      <div className="form-group">
        <label htmlFor="skills">Skills:</label>
        <input
          type="text"
          id="skills"
          name="skills"
          value={formData.skills}
          onChange={handleChange}
          placeholder="e.g., JavaScript, React, Python"
        />
      </div>

      <div className="form-group">
        <label htmlFor="experienceLevel">Experience Level:</label>
        <select
          id="experienceLevel"
          name="experienceLevel"
          value={formData.experienceLevel}
          onChange={handleChange}
          required
        >
          <option value="">Select experience level</option>
          <option value="Junior">Junior</option>
          <option value="Mid-Level">Mid-Level</option>
          <option value="Senior">Senior</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="preferredLocation">Preferred Location:</label>
        <input
          type="text"
          id="preferredLocation"
          name="preferredLocation"
          value={formData.preferredLocation}
          onChange={handleChange}
          placeholder="e.g., Remote, Bucharest"
        />
      </div>

      <div className="form-group">
        <label htmlFor="employmentType">Employment Type:</label>
        <select
          id="employmentType"
          name="employmentType"
          value={formData.employmentType}
          onChange={handleChange}
          required
        >
          <option value="">Select employment type</option>
          <option value="Full-Time">Full-Time</option>
          <option value="Part-Time">Part-Time</option>
          <option value="Freelance">Freelance</option>
          <option value="Internship">Internship</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="industry">Industry:</label>
        <input
          type="text"
          id="industry"
          name="industry"
          value={formData.industry}
          onChange={handleChange}
          placeholder="e.g., IT, Marketing, HR"
        />
      </div>

      <button type="submit">Submit</button>
    </form>
  );
}

JobSeekerPostForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  initialData: PropTypes.object, // Optional: Define expected shape if needed
};

export default JobSeekerPostForm;
