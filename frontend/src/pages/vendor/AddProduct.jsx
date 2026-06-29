import React, { useEffect, useState } from "react";
import api from '../../services/api';
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const VendorAddProduct = () => {
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    fetchCategories();
    fetchBrands();
  }, []);

  const fetchCategories = async () => {
    try {
      const res = await api.get('categories/');
      setCategories(res.data.map((item) => ({ label: item.name, value: item.id })));
    } catch (error) {
      console.error(error);
    }
  };

  const fetchBrands = async () => {
    try {
      const res = await api.get('brands/');
      setBrands(res.data.map((item) => ({ label: item.name, value: item.id })));
    } catch (error) {
      console.error(error);
    }
  };

  const productFields = [
    { name: 'name', label: 'Product Name', type: 'text' },
    { name: 'price', label: 'Product Price', type: 'number' },
    { name: 'Availability', label: 'Availability', type: 'select', options: [ { label: 'In Stock', value: 'In Stock' }, { label: 'Out of Stock', value: 'Out of Stock' } ] },
    { name: 'Condition', label: 'Condition', type: 'select', options: [ { label: 'New', value: 'New' }, { label: 'Used', value: 'Used' } ] },
    { name: 'category', label: 'Category', type: 'select', options: categories },
    { name: 'brand', label: 'Brand', type: 'select', options: brands },
    { name: 'image', label: 'Product Image', type: 'file' },
    { name: 'details', label: 'Product Details', type: 'textarea' }
  ];

  const handleProductSubmit = async (data) => {
  try {
    const formData = new FormData();

    formData.append('name', data.name);
    formData.append('price', data.price);
    formData.append('details', data.details || '');
    formData.append('Availability', data.Availability || 'In Stock');
    formData.append('Condition', data.Condition || 'New');
    formData.append('category_id', data.category);
    formData.append('brand_id', data.brand);

    if (data.image instanceof File) {
      formData.append('image', data.image);
    }

    await api.post('products/', formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`
      }
    });

    alert('Product Added Successfully!');
  } catch (error) {
    console.log(error.response?.data || error.message);
    alert('Failed to Add Product');
  }
};

  return (
    <div className="container mx-auto p-5">
      <DynamicForm title="Add Product" fields={productFields} onSubmit={handleProductSubmit} />
    </div>
  );
};

export default VendorAddProduct;
