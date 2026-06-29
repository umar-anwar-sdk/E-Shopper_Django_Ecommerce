import React from 'react';
import { useNavigate } from 'react-router-dom';

const AccessDenied = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Access Denied</h1>
        <p className="mb-4">You do not have permission to access this page.</p>
        <div className="flex gap-2 justify-center">
          <button onClick={() => navigate('/admin')} className="px-4 py-2 bg-gray-800 text-white rounded">Go to Login</button>
          <button onClick={() => navigate('/')} className="px-4 py-2 bg-blue-600 text-white rounded">Go to Home</button>
        </div>
      </div>
    </div>
  );
};

export default AccessDenied;
