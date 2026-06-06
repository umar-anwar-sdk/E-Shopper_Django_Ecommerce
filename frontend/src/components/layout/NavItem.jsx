import React from "react";

const NavItem = ({
  icon,
  title,
  collapsed,
  onClick,
  active = false,
}) => {
  return (
    <button
      onClick={onClick}
      className={`flex items-center cursor-pointer gap-3 px-4 py-3 rounded-lg w-full transition-all duration-200
      ${
        active
          ? "bg-[#dcdcdc]"
          : "bg-[#e2e2e2] hover:bg-[#cdcdcd]"
      }
      hover:translate-x-1`}
    >
      {icon}

      {!collapsed && <span>{title}</span>}
    </button>
  );
};

export default NavItem;