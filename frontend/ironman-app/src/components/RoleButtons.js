import React from 'react';
import { Button } from '@mui/material';
import '../styles/RoleButtons.css';

function RoleButtons({ role }) {
  return (
    <div className="role-buttons">
      <Button variant="contained" background-color="#007bff">Manage Orders</Button>
      {role === 'laundry-personnel' || role === 'admin' ? (
        <>
          <Button variant="contained" background-color="#007bff">Create Order</Button>
          <Button variant="contained" background-color="#007bff">Manage Society</Button>
        </>
      ) : null}
      {role === 'admin' ? (
        <Button variant="contained" background-color="#007bff">Manage Users</Button>
      ) : null}
    </div>
  );
}

export default RoleButtons;
