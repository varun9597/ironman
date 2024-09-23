import React from 'react';
import { AppBar, Toolbar, IconButton, Typography, Button } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import MenuIcon from '@mui/icons-material/Menu';
import '../styles/HeaderBar.css'; // Ensure the CSS file path is correct

const HeaderBar = () => {
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
          <Button color="inherit" className="header-button">
            <Typography variant="body1">Home</Typography>
          </Button>
          <Button color="inherit" className="header-button">
            <Typography variant="body1">About</Typography>
          </Button>
          <IconButton
            edge="end"
            className="profile-icon"
            color="inherit"
          >
            <AccountCircleIcon />
          </IconButton>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default HeaderBar;
