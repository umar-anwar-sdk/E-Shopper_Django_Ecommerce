import React from 'react'
import { FaArrowAltCircleRight } from 'react-icons/fa'

const Footer = () => {
  return (
    <>
    <div className="bg-[#1E293B]">
        <div className="container mx-auto px-4 py-16">
            <div className='font-serif text-2xl'>
                    <span className='text-[#2563EB]'>E</span>
                    <span className='text-[#ffffff]'>-SHOPPER</span>
            </div>
            <div className='text-[#ffffff] text-[12px] w-70 font-light mb-4'>Discover the latest trends, unbeatable deals, and quality products all in one place. Shop smart, shop easy.</div>
            <hr className='text-[#d6d6d0]' />
            <div className="grid grid-cols-12 mt-6">
                <div className="col-span-2">
                    <h2 className='text-[20px] text-[#ffffff] mb-3'>SERVICE</h2>
                    <ul className='text-[#ffffff] font-light leading-loose cursor-pointer'>
                        <li>Online Help</li>
                        <li>Contact us</li>
                        <li>Order Status</li>
                        <li>Change Location</li>
                        <li>FAQs</li>
                    </ul>
                </div>
                <div className="col-span-2">
                    <h2 className='text-[20px] text-[#ffffff] mb-3'>QUICK SHOP</h2>
                    <ul className='text-[#ffffff] font-light leading-loose cursor-pointer'>
                        <li>T-Shirt</li>
                        <li>Mens</li>
                        <li>Womens</li>
                        <li>Gift Cards</li>
                        <li>Shoes</li>
                    </ul>
                </div>
                <div className="col-span-2">
                    <h2 className='text-[20px] text-[#ffffff] mb-3'>POLICIES</h2>
                    <ul className='text-[#ffffff] font-light leading-loose cursor-pointer'>
                        <li>Terms of use</li>
                        <li>Privacy & Policy</li>
                        <li>Refund Policy</li>
                        <li>Billing Policy</li>
                        <li>Ticket System</li>
                    </ul>
                </div>
                <div className="col-span-2">
                    <h2 className='text-[20px] text-[#ffffff] mb-3'>ABOUT SHOPPER</h2>
                    <ul className='text-[#ffffff] font-light leading-loose cursor-pointer'>
                        <li>Company Information</li>
                        <li>Careers</li>
                        <li>Store Location</li>
                        <li>Affiliate Program</li>
                        <li>Copyright</li>
                    </ul>
                </div>
                <div className="col-span-4">
                    <h2 className='text-[20px] text-[#ffffff] mb-3'>NEWS LETTER</h2>
                    <div className="flex items-stretch ">
                        <div className='bg-gray-100 px-3 py-2 w-80'>
                            <input type="text" placeholder="Your Email Address"className="bg-transparent outline-none flex-1 text-sm"/>
                        </div>
                        <div className='bg-[#2563EB] py-2 px-3 flex items-center cursor-pointer'>
                            <FaArrowAltCircleRight className="text-[#fff] " />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </>
  )
}

export default Footer
