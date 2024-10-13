import React, { useState } from 'react';
import { AppBar, Toolbar, IconButton, Typography, Button, Menu, MenuItem } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import MenuIcon from '@mui/icons-material/Menu';
import '../../styles/HeaderBar.css'; // Ensure the CSS file path is correct
import { useNavigate } from 'react-router-dom';

const HeaderBar = () => {
  const [anchorEl, setAnchorEl] = useState(null); // State for menu anchor
  const value = sessionStorage.getItem('role');
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate('/dashboard');
  };

  // Functions to handle menu opening and closing
  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    sessionStorage.clear(); // Clear session storage on logout
    navigate('/'); // Redirect to Sign In page
    handleMenuClose(); // Close the menu
  };

  return (
    <AppBar position="static" className="header-bar">
      <Toolbar>
        <IconButton
          edge="start"
          className="menu-button"
          color="inherit"
          aria-label="menu"
        >
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" className="title">
          IronMan App
        </Typography>

        <div className="header-right">
          <Button color="inherit" className="header-button" onClick={handleHomeClick}>
            <Typography variant="body1">Home</Typography>
          </Button>
          <Button color="inherit" className="header-button">
            <Typography variant="body1">About</Typography>
          </Button>

          {/* Profile Icon with menu */}
          <IconButton
            edge="end"
            className="profile-icon"
            color="inherit"
            onClick={handleMenuOpen}
          >
            <AccountCircleIcon />
          </IconButton>
          {/* Menu */}
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default HeaderBar;
