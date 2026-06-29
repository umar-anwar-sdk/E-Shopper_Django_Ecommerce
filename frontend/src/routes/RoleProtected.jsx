import React from 'react';
import { Navigate } from 'react-router-dom';

const RoleProtected = ({ children, allowedRoles = [] }) => {
  const token = localStorage.getItem('accessToken');
  const storedRole = String(localStorage.getItem('role') || '').toLowerCase();
  const allowed = allowedRoles.map((item) => String(item).toLowerCase());

  if (!token) {
    return <Navigate to="/admin" replace />;
  }

  if (allowed.length > 0 && !allowed.includes(storedRole)) {
    return <Navigate to="/access-denied" replace />;
  }

  return children;
};

export default RoleProtected;
