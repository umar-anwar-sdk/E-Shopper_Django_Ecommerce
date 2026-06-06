import React, { useEffect, useState } from 'react'
import { FaCartPlus, FaRegCalendarAlt, FaUserAlt } from 'react-icons/fa';
import BorderedHeading from '../../components/common/websitecommon/BorderedHeading';
import { FaRegCalendarDays } from 'react-icons/fa6';
import ProductSlider from '../../components/common/websitecommon/ProductSlider';

const ProductDetails = () => {

    return (
    <>
        <div className="container px-4 mx-auto mt-6 my-6">
            <BorderedHeading heading={"product details"} />
            <div className="grid grid-cols-12 gap-7 mb-20">
                <div className='col-span-4 border-2 border-[#f5f5f5]'>
                    
                    <img src="" className='w-full h-full' alt="Product Image" />
                </div>
                <div className='col-span-8 relative border-2 border-[#f5f5f5] p-10'>
                    {/* Badge */}
                    <div className="absolute top-0 left-0 text-white bg-red-600 text-sm px-2 cursor-pointer">
                        New
                    </div>
                    <h2 className='text-2xl mb-3 '>Laptop</h2>
                    <p className='text-sm mb-3'>4 Years ago</p>
                    <div className='flex items-center justify-between mb-4'>
                        <div className='text-3xl font-bold text-[#1E293B]'>PKR 30000/-</div>
                        <div>
                            Quantity: <input type="number" className='border-1 p-3 w-20 ms-2 border-[#f5f5f5] focus:outline-0' />
                        </div>
                        <div>
                            <button className='bg-[#1E293B] flex items-center border-0 p-3 px-4 text-white cursor-pointer text-sm'><FaCartPlus className='text-lg me-1' /> Add to Cart</button>
                        </div>
                    </div>
                    <div className='flex items-center gap-4'>
                        <span className='text-lg font-semibold'>Availability:</span>
                        <span>In Stock</span>
                    </div>
                    <div className='flex items-center gap-4'>
                        <span className='text-lg font-semibold'>Specification:</span>
                        <span>8 gb ram\r\n1 tera bite hard</span>
                    </div>
                    <div className='flex items-center gap-4'>
                        <span className='text-lg font-semibold'>Brand:</span>
                        <span>HP</span>
                    </div>
                </div>
            </div>
            <div className='grid grid-cols-12 gap-5'>
                <div className='col-span-6'>
                    <BorderedHeading heading={"Reviews"} />
                    <div className='border-2 border-[#f5f5f5] shadow-lg p-4 mb-4'>
                        <div className='flex items-center gap-5 mb-4'>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaUserAlt /></span>
                                <span>Henry Bey</span>
                            </div>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaRegCalendarDays /></span>
                                <span>31 Dec, 2022</span>
                            </div>
                        </div>
                        <p className=''>So nice</p>
                    </div>
                    <div className='border-2 border-[#f5f5f5] shadow-lg p-4 mb-4'>
                        <div className='flex items-center gap-5 mb-4'>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaUserAlt /></span>
                                <span>Henry Bey</span>
                            </div>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaRegCalendarDays /></span>
                                <span>31 Dec, 2022</span>
                            </div>
                        </div>
                        <p className=''>Pretty</p>
                    </div>
                    <div className='border-2 border-[#f5f5f5] shadow-lg p-4 mb-4'>
                        <div className='flex items-center gap-5 mb-4'>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaUserAlt /></span>
                                <span>Henry Bey</span>
                            </div>
                            <div className='flex items-center gap-1 text-sm text-[#2563EB]'>
                                <span><FaRegCalendarDays /></span>
                                <span>31 Dec, 2022</span>
                            </div>
                        </div>
                        <p className=''>Pretty</p>
                    </div>
                </div>
                <div className='col-span-6'>
                    <BorderedHeading heading={"Write Your Review"} />
                    <form action="">
                        <div className='flex items-center justify-between gap-5 mb-3'>
                            <input type="text" className='border border-[#f5f5f5] p-2 focus:outline-[#2563EB] hover:border-[#2563EB] w-full' placeholder='Your name'/>
                            <input type="email" className='border border-[#f5f5f5] p-2 focus:outline-[#2563EB] hover:border-[#2563EB] w-full' placeholder='Your Email' />
                        </div>
                        <textarea name="" id="" rows={4} placeholder='Subject' className='w-full p-2 border border-[#f5f5f5] hover:border-[#2563EB] focus:outline-[#2563EB] mb-3'></textarea>
                        <button className='bg-[#1E293B] p-2 text-white text-sm float-end'>Submit</button>
                    </form>
                </div>
            </div>
            <BorderedHeading  heading={"our recommended items"} />
            {/* <ProductSlider /> */}
        </div>
    </>
  )
}

export default ProductDetails
