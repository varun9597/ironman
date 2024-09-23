import React from 'react';
import ProfileTooltip from './ProfileTooltip';
import '../styles/SideMenu.css';

function SideMenu() {
  return (
    <div className="side-menu">
      <div className="profile-icon">
        <ProfileTooltip />
      </div>
    </div>
  );
}

export default SideMenu;
