import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import WebsiteRoutes from './WebsiteRoutes';
import AdminRoutes from './AdminRoutes';

const LoadingPage = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
  </div>
);

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/*" element={<WebsiteRoutes />} />
      <Route path="/admin/*" element={<AdminRoutes />} />
    </Routes>
  );
};

export default AppRoutes;
