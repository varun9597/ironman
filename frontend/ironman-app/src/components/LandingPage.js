import React, { useState } from 'react';
import Header from './Header';
import SignInForm from './SignInForm';

function LandingPage() {
  const [showSignIn, setShowSignIn] = useState(false);

  return (
    <div className="landing-page">
      <Header />
      <div className="content">
        {!showSignIn ? (
          <>
            <p className="description">
              Welcome to the <span className="highlight">IronMan App</span>. A sleek, powerful platform designed to manage your societies, orders, and rate cards efficiently. Sign up to get started or log in to continue.
            </p>
            <div className="buttons">
              <button className="btn sign-in" onClick={() => setShowSignIn(true)}>Sign In</button>
              <button className="btn register">Register</button>
            </div>
          </>
        ) : (
          <SignInForm />
        )}
      </div>
    </div>
  );
}

export default LandingPage;
