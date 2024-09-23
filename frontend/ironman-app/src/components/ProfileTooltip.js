import React, { useState } from 'react';
import { Tooltip, IconButton, MenuItem, Menu } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

function ProfileTooltip() {
  const [anchorEl, setAnchorEl] = useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <>
      <Tooltip title="Profile">
        <IconButton onClick={handleClick}>
          <AccountCircleIcon fontSize="large" />
        </IconButton>
      </Tooltip>
      <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
        <MenuItem onClick={handleClose}>Manage Profile</MenuItem>
        <MenuItem onClick={handleClose}>Logout</MenuItem>
      </Menu>
    </>
  );
}

export default ProfileTooltip;
