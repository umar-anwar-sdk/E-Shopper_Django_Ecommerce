import React, { useEffect, useState } from 'react'
import BannerSlider from '../../components/common/websitecommon/BannerSlider';
import ProductCards from '../../components/common/websitecommon/ProductCards';
import BorderedHeading from '../../components/common/websitecommon/BorderedHeading';

const Home = ({ heading }) => {

  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedBrand, setSelectedBrand] = useState("");

  useEffect(() => {
    fetchCategories();
    fetchBrands();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await fetch("https://umaranwar.pythonanywhere.com/api/categories");
      const data = await res.json();

      setCategories(Array.isArray(data) ? data : []);
    } catch (error) {
      console.log("Category Error:", error);
      setCategories([]);
    }
  };

  const fetchBrands = async () => {
    try {
      const res = await fetch("https://umaranwar.pythonanywhere.com/api/brands");
      const data = await res.json();

      setBrands(Array.isArray(data) ? data : []);
    } catch (error) {
      console.log("Brand Error:", error);
      setBrands([]);
    }
  };

  return (
    <div>
      <BannerSlider />

      <div className="container px-4 mx-auto mt-6 my-6">
        <div className="grid grid-cols-12 gap-10">

          <div className="col-span-12 my-5">

            <div className='flex items-center justify-between mb-4'>

              <h1 className='text-2xl font-bold text-[#1E293B]'>
                Featured Products
              </h1>

              <div className="flex gap-4 mb-6">

                {/* Category Filter */}
                <select
                  className="border p-2"
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                  <option value="">All Categories</option>

                  {categories?.map((cat) => (
                    <option key={cat.id} value={cat.id}>
                      {cat.name}
                    </option>
                  ))}
                </select>

                {/* Brand Filter */}
                <select
                  className="border p-2"
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                >
                  <option value="">All Brands</option>

                  {brands?.map((brand) => (
                    <option key={brand.id} value={brand.id}>
                      {brand.name}
                    </option>
                  ))}
                </select>

              </div>
            </div>

            <ProductCards
              selectedCategory={selectedCategory}
              selectedBrand={selectedBrand}
            />

          </div>
        </div>
      </div>
    </div>
  )
}

export default Home