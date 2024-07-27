import React, { useState, useEffect } from 'react';
import axios from 'axios';

const GymPerformance = () => {
  const [performances, setPerformances] = useState([]);
  const [date, setDate] = useState('');
  const [performance, setPerformance] = useState('');

  useEffect(() => {
    const fetchPerformances = async () => {
      const response = await axios.get('http://localhost:5000/performance', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setPerformances(response.data.performances);
    };
    fetchPerformances();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post(
      'http://localhost:5000/performance',
      { date, performance },
      {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      }
    );
    setPerformances([...performances, { date, performance }]);
  };

  return (
    <div>
      <h2>Track Your Gym Performance</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          placeholder="Date"
        />
        <input
          type="text"
          value={performance}
          onChange={(e) => setPerformance(e.target.value)}
          placeholder="Performance"
        />
        <button type="submit">Add Performance</button>
      </form>
      <h3>Your Performances</h3>
      <ul>
        {performances.map((p, index) => (
          <li key={index}>
            {p.date}: {p.performance}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default GymPerformance;
