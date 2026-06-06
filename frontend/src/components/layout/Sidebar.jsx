import React from "react";
import logo from "../../assets/logo.png";
import {
  LayoutDashboard,
  ShoppingCart,
  Settings,
} from "lucide-react";
import { IoLayersOutline } from "react-icons/io5";

import NavItem from "./NavItem";
import { MdOutlineBrandingWatermark } from "react-icons/md";
import { useNavigate, useLocation } from 'react-router-dom';

const Sidebar = ({ collapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <aside
      className={`fixed left-0 top-0 h-screen bg-[#f5f5f5] text-gray-800 shadow-2xl transition-all duration-300 z-50
      ${collapsed ? "w-20" : "w-64"}`}
    >
      {/* Logo */}
      <div className="p-4 flex justify-center">
        {!collapsed && (
          <img
            src={logo}
            width="150"
            alt="Logo"
          />
        )}
      </div>

      <div className="p-4 space-y-3">
        <NavItem
          icon={<LayoutDashboard size={20} />}
          title="Dashboard"
          collapsed={collapsed}
          onClick={() => navigate('/admin/dashboard')}
          active={isActive('/admin/dashboard')}
        />

        <NavItem
          icon={<ShoppingCart size={20} />}
          title="Products"
          collapsed={collapsed}
          onClick={() => navigate('/admin/dashboard/products')}
          active={isActive('/admin/dashboard/products')}
        />

        <NavItem
          icon={<IoLayersOutline size={20} />}
          title="Categories"
          collapsed={collapsed}
          onClick={() => navigate('/admin/dashboard/categories')}
          active={isActive('/admin/dashboard/categories')}
        />

        <NavItem
          icon={<MdOutlineBrandingWatermark size={20} />}
          title="Brands"
          collapsed={collapsed}
          onClick={() => navigate('/admin/dashboard/brands')}
          active={isActive('/admin/dashboard/brands')}
        />

        <NavItem
          icon={<Settings size={20} />}
          title="Settings"
          collapsed={collapsed}
          onClick={() => navigate('/admin/dashboard/settings')}
          active={isActive('/admin/dashboard/settings')}
        />
      </div>
    </aside>
  );
};

export default Sidebar;