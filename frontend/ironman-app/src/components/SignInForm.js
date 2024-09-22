import React, { useState } from 'react';
import axios from 'axios';
import '../styles/SignInForm.css';


function SignInForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState(null);

  const handleSignIn = async () => {
    try {
        const response = await axios.post('http://127.0.0.1:5000/signin_auth', {
            username,
            password,
          });
      console.log('Login successful:', response.data);
    } catch (err) {
      setError('Failed to sign in.');
    }
  };

  return (
    <div className="signin-form">
      <h2>Sign In</h2>
      <div className="form-group">
        <label htmlFor="username">Username</label>
        <input
          type="text"
          id="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">Password</label>
        <input
          type={showPassword ? 'text' : 'password'}
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      <div className="form-group show-password">
        <input
          type="checkbox"
          id="showPassword"
          checked={showPassword}
          onChange={() => setShowPassword(!showPassword)}
        />
        <label htmlFor="showPassword">Show Password</label>
      </div>
      <button
        className="btn sign-in"
        onClick={handleSignIn}
        disabled={!username || !password}
      >
        Sign In
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default SignInForm;
