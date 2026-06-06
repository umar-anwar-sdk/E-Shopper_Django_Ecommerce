import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { getAllProducts } from '../../../services/productsService';

const ProductCards = ({ selectedCategory, selectedBrand }) => {

  const navigate = useNavigate();
  const [productsData, setProductsData] = useState([]);

  const getProductsData = async () => {
    try {
      const data = await getAllProducts();
      setProductsData(data);
    } catch (error) {
      console.error("API Error:", error);
    }
  };

  useEffect(() => {
    getProductsData();
  }, []);

  const filteredProducts = productsData.filter((product) => {
    

    const matchCategory = selectedCategory
      ? product.category == selectedCategory || product.category?.category == selectedCategory
      : true;

    const matchBrand = selectedBrand
      ? product.brand == selectedBrand || product.brand?.name == selectedBrand
      : true;

    return matchCategory && matchBrand;
  });

  return (
    <div className="container mx-auto px-4">
      <div className="grid grid-cols-12 gap-5 py-5 items-stretch">

        {filteredProducts.map((product, index) => (
          <div key={index} className="col-span-3 mb-4 flex shadow-xl">

            <div className="bg-white text-center group relative overflow-hidden border border-[#f5f5f5] flex flex-col w-full">

              {/* Image */}
              <div className="relative overflow-hidden">
                <img
                  src={product.image}
                  className="w-full h-70 object-cover"
                  alt=""
                />
              </div>

              {/* Content */}
              <div className="text-left p-3 flex flex-col flex-grow">
                
                <div className="text-[#2563EB] text-center text-xl font-bold">
                  {product.price}/-
                </div>

                <h3 
                  onClick={() => navigate(`/details`)} 
                  className="text-lg text-center font-semibold text-[#1E293B] mb-4 cursor-pointer"
                >
                  {product.name}
                </h3>

                <div className="flex items-center justify-center">
                  <button className="bg-[#1E293B] hover:bg-[#2563EB] w-full text-white text-xs p-2 cursor-pointer">
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}

        {filteredProducts.length === 0 && (
          <div className="col-span-12 text-center text-gray-500">
            No products found
          </div>
        )}

      </div>
    </div>
  )
}

export default ProductCards;