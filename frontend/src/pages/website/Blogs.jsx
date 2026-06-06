import React from 'react'
import BorderedHeading from '../../components/common/websitecommon/BorderedHeading'

const Blogs = () => {
  return (
    <>
      <div className="container px-4 mx-auto mt-6 my-6">
        <div className="grid grid-cols-12 gap-10">
            <div className="col-span-9">
                <BorderedHeading heading={"latest from our blogs"} />
            </div>
        </div>
      </div>
    </>
  )
}

export default Blogs
