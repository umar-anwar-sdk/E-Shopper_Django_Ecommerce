import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import RoleProtected from './RoleProtected';
import VendorDashboard from '../pages/vendor/Dashboard';
import VendorProducts from '../pages/vendor/Products';
import VendorAddProduct from '../pages/vendor/AddProduct';
import VendorProfile from '../pages/vendor/Profile';
import EditProduct from '../pages/vendor/EditProduct';

const VendorRoutes = () => {
  return (
    <Routes>
      <Route path="" element={<Navigate to="/vendor/dashboard" replace />} />
      <Route
        path="dashboard"
        element={
          <RoleProtected allowedRoles={["vendor"]}>
            <DashboardLayout />
          </RoleProtected>
        }
      >
        <Route index element={<VendorDashboard />} />
        <Route path="products" element={<VendorProducts />} />
        <Route path="add-product" element={<VendorAddProduct />} />
        <Route path="products/edit/:productId" element={<EditProduct />} />
        <Route path="profile" element={<VendorProfile />} />
      </Route>
      <Route path="*" element={<Navigate to="/vendor/dashboard" replace />} />
    </Routes>
  );
};

export default VendorRoutes;
