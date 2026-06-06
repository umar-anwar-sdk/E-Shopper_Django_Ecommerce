import React from 'react'
import ProductCards from '../../components/common/websitecommon/ProductCards';
import BorderedHeading from '../../components/common/websitecommon/BorderedHeading'

const Products = () => {
  return (
    <>
        <div className="container mx-auto px-4">
          <BorderedHeading heading={"All Products"} />
          <ProductCards />
        </div>
    </>
  )
}

export default Products
