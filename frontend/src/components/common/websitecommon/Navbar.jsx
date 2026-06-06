import React, { useEffect, useState } from 'react'
import { BsTwitterX } from 'react-icons/bs'
import { FaCrosshairs, FaFacebookF, FaLinkedinIn, FaLock, FaSearch, FaUser } from 'react-icons/fa'
import { FiGlobe } from 'react-icons/fi'
import { MdCall, MdEmail, MdStar } from 'react-icons/md'
import { TfiGoogle } from 'react-icons/tfi'
import logo from "../../../assets/logo.png";
import { IoMdCart } from 'react-icons/io'
import { Link, useNavigate } from 'react-router-dom'

const Navbar = () => {

    const [isOpen, setIsOpen] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
      // Check if user is logged in
      const token = localStorage.getItem('token');
      setIsLoggedIn(!!token);
    }, []);

    const handleLogout = () => {
      localStorage.removeItem('token');
      setIsLoggedIn(false);
      navigate('/');
    };

    const handleAdminClick = () => {
      navigate('/admin/dashboard');
    };

    const socialIcons = [
        { icon: <FaFacebookF />, link: "" },
        { icon: <BsTwitterX />, link: "" },
        { icon: <FaLinkedinIn />, link: "" },
        { icon: <FiGlobe />, link: "" },
        { icon: <TfiGoogle />, link: "" },
    ];
  return (
    <>
    {/* header */}
    
    <div className="bg-[#1E293B] text-[#2563EB]">
        <div className='container '></div>
        <div className="container px-4 mx-auto">
            <div className="flex items-center justify-between h-10">
                <div className="flex items-center gap-5">
                    <div className='flex items-center gap-1'>
                        <span><MdCall /></span>
                        <span className='text-sm'>+92 329 0017770</span>
                    </div>
                    <div className='flex items-center gap-1'>
                        <span><MdEmail /></span>
                        <span className='text-sm'>ayeshakainat523@gmail.com</span>
                    </div>
                </div>
                <div className="flex items-center gap-5">
                    {socialIcons.map((item, index) => (
                        <a key={index} href={item.link} target='_blank' className="p-2 rounded-full hover:bg-[#2563EB] hover:text-white transition duration-300">{item.icon}</a>
                    ))}
                </div>
            </div>
        </div>
    </div>
    {/* navbar */}
    <div className="container mx-auto px-4">
        <div className="">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 px-8">
                <div className="flex flex-col md:flex-row md:justify-between md:items-center h-auto md:h-16 gap-4 md:gap-0 my-4 md:my-0">
                {/* Logo */}
                <div className="flex justify-center md:justify-start">
                    <img src={logo} width={200} alt="" />
                </div>
                {/* Links */}
                <div className="flex space-x-8 items-center justify-between text-[#1E293B] gap-3 md:gap-0">
                    <a href="#" className="hover:text-[#2563EB] flex items-center gap-1">
                        <span className='text-sm'><FaUser /></span>
                        <span className='text-sm'>Account</span>
                    </a>
                    <a href="#" className="hover:text-[#2563EB] flex items-center gap-1">
                        <span className='text-sm'><MdStar /></span>
                        <span className='text-sm'>Wishlist</span>
                    </a>
                    <a href="#" className="hover:text-[#2563EB] flex items-center gap-1">
                        <span className='text-sm'><FaCrosshairs /></span>
                        <span className='text-sm'>Checkout</span>
                    </a>
                    <a href="#" className="hover:text-[#2563EB] flex items-center gap-1">
                        <span className='text-sm'><IoMdCart /></span>
                        <span className='text-sm'>Cart</span>
                    </a>

                    {isLoggedIn ? (
                      <>
                        <button onClick={handleAdminClick} className="hover:text-[#2563EB] flex items-center gap-1">
                            <span className='text-sm'><FaUser /></span>
                            <span className='text-sm'>Admin</span>
                        </button>
                        <button onClick={handleLogout} className="hover:text-[#2563EB] flex items-center gap-1">
                            <span className='text-sm'><FaLock /></span>
                            <span className='text-sm'>Logout</span>
                        </button>
                      </>
                    ) : (
                      <Link to="/admin" className="hover:text-[#2563EB] flex items-center gap-1">
                          <span className='text-sm'><FaLock /></span>
                          <span className='text-sm'>Login</span>
                      </Link>
                    )}
                </div>
            </div>
            </div>
        </div>
        <hr className='text-[#cdcdcd]' />

        <nav className="">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Desktop Menu */}
                    <div className="hidden md:flex space-x-8 items-center">
                        <Link to={"/"}  className="text-[#1E293B] hover:text-[#2563EB]">Home</Link>
                        <Link to={"/products"}  className="text-[#1E293B] hover:text-[#2563EB]">Products</Link>
                        <Link to={"/blogs"} className="text-[#1E293B] hover:text-[#2563EB]">Blogs</Link>
                        <Link to={"/contact"} className="text-[#1E293B] hover:text-[#2563EB]">Contact</Link>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="text-[#1E293B] cursor-pointer">
                            <FaSearch />
                        </span>
                    </div>
                    {/* Mobile Button */}
                    <div className="md:hidden">
                        <button onClick={() => setIsOpen(!isOpen)} className="text-[#696763] focus:outline-none">
                            {isOpen ? (
                                <span className="text-2xl">&times;</span>
                            ) : (
                                <span className="text-2xl">&#9776;</span>
                            )}
                        </button>
                    </div>
                </div>
            </div>
            {/* Mobile Menu */}
            <div className={`md:hidden bg-white px-4 pt-2 pb-4 space-y-3 transition-all duration-300 ${
            isOpen ? "block" : "hidden"}`}>
                <Link to="/" className="block text-[#696763] hover:text-[#2563EB]">Home</Link>
                <Link to="/products" className="block text-[#696763] hover:text-[#2563EB]">Products</Link>
                <Link to="/blogs" className="block text-[#696763] hover:text-[#2563EB]">Blogs</Link>
                <Link to="/contact" className="block text-[#696763] hover:text-[#2563EB]">Contact</Link>
            </div>
        </nav>
    </div>
    </>
  )
}

export default Navbar
