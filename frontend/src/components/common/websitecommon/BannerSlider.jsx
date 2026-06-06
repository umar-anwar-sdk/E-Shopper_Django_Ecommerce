import React from 'react'
import { Swiper, SwiperSlide } from "swiper/react";
import { Autoplay, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/pagination";
import banner1 from "../../../assets/banner1.jpg";
import banner2 from "../../../assets/banner2.jpg";
import banner3 from "../../../assets/banner3.jpg";


const BannerSlider = () => {
  const images = [
    banner1,
    banner2,
    banner3,

];
  return (
    <>
      <div className=" mx-auto">
        <Swiper
          modules={[Autoplay, Pagination]}
          loop={true}
          autoplay={{ delay: 2500 }}
          spaceBetween={20}
          pagination={{ clickable: true }}
          style={{
              "--swiper-pagination-color": "#1E293B",
              "--swiper-pagination-bullet-inactive-color": "#999",
            }}
          breakpoints={{
            480: { slidesPerView: 1 },
            767: { slidesPerView: 1 },
            1024: { slidesPerView: 1 },
            1366: { slidesPerView: 1 },
          }}
        >
          {images.map((img, index) => (
            <SwiperSlide key={index}>
              <div className="w-full h-[500px] bg-center bg-cover bg-no-repeat" style={{ backgroundImage: `url(${img})`,}}>
                <div className="container mx-auto">
                  <div className='grid grid-cols-12 '>
                    <div className='col-span-6 mt-35'>
                      <h1 className='text-5xl font-bold mb-5 text-[#2563EB]'>Shop the Latest Trends</h1>
                      <h1 className='text-3xl mb-3 text-[#1E293B]'>Upgrade Your Style Today</h1>
                      <p className='font-extralight'>Discover fashion that defines you. From casual wear to premium outfits, explore collections designed to keep you ahead of the trend.</p>
                    </div>
                  </div>
                </div>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </>
  )
}

export default BannerSlider
