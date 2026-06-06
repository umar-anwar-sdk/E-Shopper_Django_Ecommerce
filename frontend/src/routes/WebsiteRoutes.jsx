import React from 'react';
import { Route, Routes } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import Home from '../pages/website/Home';
import Products from '../pages/website/Products';
import ProductDetails from '../pages/website/ProductDetails';
import Blogs from '../pages/website/Blogs';
import Contact from '../pages/website/Contact';

const LoadingPage = () => (
  <div className="flex items-center justify-center min-h-screen">
    <div className="flex items-center justify-center">
      <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
    </div>
  </div>
);

const WebsiteRoutes = () => {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:id" element={<ProductDetails />} />
        <Route path="/blogs" element={<Blogs />} />
        <Route path="/contact" element={<Contact />} />
      </Route>
    </Routes>
  );
};

export default WebsiteRoutes;
