import React from 'react';
import { useLocation } from 'react-router-dom';
import RoleButtons from '../components/RoleButtons';
import HeaderBar from '../components/HeaderBar'; // Import HeaderBar
import '../styles/Dashboard.css';

function Dashboard() {
  const location = useLocation();
  const { role } = location.state; // Get role from the landing page navigation

  return (
    <div className="dashboard-layout">
      <HeaderBar /> {/* Add the HeaderBar at the top */}

      {/* <div className="main-layout">
        <SideMenu /> Keep the side menu for navigation */}

        <div className="dash-content">
          <h2>Welcome to the Dashboard</h2>
          <RoleButtons role={role} /> {/* Show role-based buttons */}
        </div>
      </div>
    // </div>
  );
}

export default Dashboard;
