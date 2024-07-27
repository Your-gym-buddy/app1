import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div>
      <h1>Welcome to the Gym Tracker App</h1>
      <Link to="/login">Login</Link>
      <Link to="/signup">Signup</Link>
    </div>
  );
};

export default LandingPage;
