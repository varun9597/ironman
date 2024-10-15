import React from 'react';
import { Button } from '@mui/material';
import '../styles/RoleButtons.css';
import { useNavigate } from 'react-router-dom';

function RoleButtons({ role }) {
  const navigate = useNavigate();
  const handleManageSocietyClick = () => {
    navigate('/manage-society');
  };

  const handleManageUsersClick = () => {
    navigate('/manage-users');
  }


  return (
    <div className="role-buttons">
      <Button variant="contained" background-color="#007bff">Manage Orders</Button>
      {role === 'laundry-personnel' || role === 'admin' ? (
        <>
          {/* <Button variant="contained" background-color="#007bff">Create Order</Button> */}
          <Button variant="contained" background-color="#007bff" onClick={handleManageSocietyClick}>Manage Society</Button>
        </>
      ) : null}
      {role === 'admin' ? (
        <Button variant="contained" background-color="#007bff" onClick={handleManageUsersClick}>Manage Users</Button>
      ) : null}
    </div>
  );
}

export default RoleButtons;
