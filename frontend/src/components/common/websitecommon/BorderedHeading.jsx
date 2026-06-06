import React from 'react'

const BorderedHeading = ({heading}) => {
  return (
    <div>
      <div className="flex items-center justify-between w-full gap-2 my-4 text-xl font-semibold text-[#1E293B]">
            <span className='bg-[#f5f5f5] w-full h-[2px]'></span>
            <span className='uppercase text-nowrap'>{heading}</span>
            <span className='bg-[#f5f5f5] w-full h-[2px]'></span>
        </div>
    </div>
  )
}

export default BorderedHeading
