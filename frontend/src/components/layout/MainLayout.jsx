import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from '../common/websitecommon/Navbar'
import Footer from '../common/websitecommon/Footer'

const MainLayout = () => {
  return (
    <div>
      <Navbar />
      <Outlet />
      <Footer />
    </div>
  )
}

export default MainLayout
