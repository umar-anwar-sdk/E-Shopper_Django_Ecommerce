import React from 'react'
import { BsTwitterX } from 'react-icons/bs';
import { FaFacebookF, FaLinkedinIn } from 'react-icons/fa';
import { FiGlobe } from 'react-icons/fi';
import { TfiGoogle } from 'react-icons/tfi';
import BorderedHeading from '../../components/common/websitecommon/BorderedHeading';

const Contact = () => {
    const socialIcons = [
        { icon: <FaFacebookF />, link: "" },
        { icon: <BsTwitterX />, link: "" },
        { icon: <FaLinkedinIn />, link: "" },
        { icon: <FiGlobe />, link: "" },
        { icon: <TfiGoogle />, link: "" },
    ];
  return (
    <>
    <div className="container mx-auto px-4 my-16">
        <BorderedHeading heading={"contact us"} />
        <div className="grid grid-cols-12 gap-5 my-10">
            <div className="col-span-7">
                <BorderedHeading heading={"get in touch"} />
                <div className='my-5'>
                    <form action="">
                        <div className='flex items-center justify-between gap-5 w-full mb-4'>
                            <input type="text" className='border border-[#f5f5f5] hover:border-[#1E293B] w-full p-2' placeholder='Name'/>
                            <input type="email" className='border border-[#f5f5f5] hover:border-[#1E293B] w-full p-2' placeholder='Email' />
                        </div>
                        <div className='mb-4'>
                            <input type="text" className='border border-[#f5f5f5] hover:border-[#1E293B] w-full p-2' placeholder='Subject' />
                        </div>
                        <div className='mb-4'>
                            <textarea name="" rows={6} className='border border-[#f5f5f5] hover:border-[#1E293B] w-full p-2'  placeholder='Your Message here' ></textarea>
                        </div>
                        <div>
                            <button className='bg-[#1E293B] px-3 py-2 cursor-pointer text-white ms-auto'>Submit</button>
                        </div>
                    </form>
                </div>
            </div>
            <div className="col-span-5">
                <BorderedHeading heading={"contact info"} />
                <div className='mt-5 leading-10 px-3'>
                    <p>E-Shopper Inc.</p>
                    <p>935 W. Webster Ave New Streets Chicago,</p>
                    <p>IL 60614, NY</p>
                    <p>Newyork USA</p>
                    <p>Mobile: +2346 17 38 93</p>
                    <p>Fax: 1-714-252-0026</p>
                    <p>Email: info@e-shopper.com</p>
                </div>
                <BorderedHeading heading={"social networks"} />
                <div className="flex items-center justify-center text-lg gap-5">
                    {socialIcons.map((item, index) => (
                        <a key={index} href={item.link} target='_blank' className="p-2 rounded-full hover:bg-[#1E293B] hover:text-white transition duration-300">{item.icon}</a>
                    ))}
                </div>
            </div>
        </div>
    </div>
    </>
  )
}

export default Contact
