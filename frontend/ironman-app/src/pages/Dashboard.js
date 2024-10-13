import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import RoleButtons from '../components/RoleButtons';
import HeaderBar from '../components/HeaderBar/HeaderBar'; // Import HeaderBar
import '../styles/Dashboard.css';
import {jwtDecode} from 'jwt-decode'; // Make sure to remove the curly braces for correct import

function Dashboard() {
  const navigate = useNavigate();
  
  // Local state to store role and user_id
  const [role, setRole] = useState(null);
  const [userId, setUserId] = useState(null);
  const [loading, setLoading] = useState(true); // State to manage loading

  useEffect(() => {
    const access_token = sessionStorage.getItem('access_token');

    if (!access_token) {
      // If no token is found, redirect to the sign-in page
      navigate('/');
      return;
    }

    try {
      // Decode the token and extract role and user_id
      const decodedToken = jwtDecode(access_token);
      const userRole = decodedToken.sub.role;
      const userId = decodedToken.sub.user_id; // Assuming sub is user_id

      // Set role and userId in local state
      setRole(userRole);
      setUserId(userId);

      // Store in sessionStorage for future use
      sessionStorage.setItem('user_id', userId);
      sessionStorage.setItem('role', userRole);
    } catch (error) {
      console.error('Invalid token:', error);
      navigate('/');
    } finally {
      setLoading(false); // Once decoding is done, stop loading
    }
  }, [navigate]);

  // Show loading until role is set
  if (loading) {
    return <p>Loading...</p>;
  }

  return (
    <div className="dashboard-layout">
      <HeaderBar /> {/* Add the HeaderBar at the top */}

      <div className="dash-header">
        <h2>Welcome to the Dashboard</h2>
      </div>

      <div className="dash-content">
        {role ? (
          <RoleButtons role={role} /> // Show role-based buttons when the role is set
        ) : (
          <p>No role found</p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
