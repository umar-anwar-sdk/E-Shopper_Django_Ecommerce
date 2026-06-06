import React from "react";
import { useNavigate } from "react-router-dom";
import { Menu } from "lucide-react";
import { IoIosLogOut } from "react-icons/io";

const Header = ({ collapsed, setCollapsed }) => {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };
  return (
    <header
      className={`fixed top-0 right-0 h-16 bg-white shadow px-4 flex items-center gap-4 z-40 transition-all duration-300
      ${collapsed ? "md:left-20" : "md:left-64"} left-0`}
    >
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="p-2 rounded hover:bg-gray-100"
      >
        <Menu size={22} />
      </button>

      <h2 className="font-semibold text-lg">
        Dashboard
      </h2>
      <button
        onClick={handleLogout}
        className="ml-auto flex items-center text-black text-2xl hover:bg-gray-100 py-2 px-4 rounded gap-1 cursor-pointer"
      >
       <IoIosLogOut />
      </button>
    </header>
  );
};

export default Header;