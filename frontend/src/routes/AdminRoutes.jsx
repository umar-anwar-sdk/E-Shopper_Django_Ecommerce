import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import ProtectedRoutes from './ProtectedRoutes';
import RoleProtected from './RoleProtected';
import Login from '../pages/login/login';
import Products from '../pages/dashboard/products';
import AddProduct from '../pages/dashboard/AddProduct';
import AddBrand from '../pages/dashboard/AddBrand';
import AddCategory from '../pages/dashboard/AddCategory';
import Categories from '../pages/dashboard/Categories';
import Brands from '../pages/dashboard/Brands';
import DashboardHome from '../pages/dashboard/DashboardHome';
import EditCategory from '../pages/dashboard/EditCategory';
import EditBrands from '../pages/dashboard/EditBrands';
import Vendors from '../pages/dashboard/Vendors';
import AddVendor from '../pages/dashboard/AddVendor';
import EditVendor from '../pages/dashboard/EditVendor';
import VendorDetails from '../pages/dashboard/VendorDetails';

// Loading component
const LoadingPage = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="flex items-center justify-center">
        <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
</div>
);


const AdminRoutes = () => {
  return (
      <Routes>
        <Route path="" element={<Login />} />
        <Route
          path="dashboard"
          element={
              <RoleProtected allowedRoles={["admin"]}>
                <ProtectedRoutes>
                  <DashboardLayout />
                </ProtectedRoutes>
              </RoleProtected>
            }
        >
          <Route index element={<DashboardHome />} />
          <Route path="products" element={<Products />} />
          <Route path="products/add" element={<AddProduct />} />
          <Route path="vendors" element={<Vendors />} />
          <Route path="vendors/add" element={<AddVendor />} />
          <Route path="vendors/edit/:id" element={<EditVendor />} />
          <Route path="vendors/:id" element={<VendorDetails />} />
          <Route path="categories" element={<Categories />} />
          <Route path="brands" element={<Brands />} />
          <Route path="brands/add" element={<AddBrand />} />
          <Route path="categories/add" element={<AddCategory />} /> 
          <Route path="categories/edit/:id" element={<EditCategory />} />
          <Route path="brands/edit/:id" element={<EditBrands />} />
        </Route>
        
        <Route path="*" element={<Navigate to="/admin" replace />} />
      </Routes>
  );
};

export default AdminRoutes;
