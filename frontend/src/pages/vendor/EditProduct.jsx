import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import api from '../../services/api';
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const EditProduct = () => {
  const { productId } = useParams();

  const [initialValues, setInitialValues] = useState({});
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    fetchCategories();
    fetchBrands();

    if (productId) {
      fetchProduct();
    }
  }, [productId]);

  const fetchCategories = async () => {
    const res = await api.get('categories/');
    setCategories(res.data.map(i => ({ label: i.name, value: i.id })));
  };

  const fetchBrands = async () => {
    const res = await api.get('brands/');
    setBrands(res.data.map(i => ({ label: i.name, value: i.id })));
  };

  const fetchProduct = async () => {
    try {
      const res = await api.get(`products/${productId}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      });

      const product = res.data;

      setInitialValues({
        name: product.name,
        price: product.price,
        details: product.details,
        Availability: product.Availability,
        Condition: product.Condition,
        category: product.category?.id,
        brand: product.brand?.id,
      });

    } catch (error) {
      console.error(error);
    }
  };

  const productFields = [
    { name: 'name', label: 'Product Name', type: 'text' },
    { name: 'price', label: 'Product Price', type: 'number' },
    { name: 'Availability', label: 'Availability', type: 'select', options: [
      { label: 'In Stock', value: 'In Stock' },
      { label: 'Out of Stock', value: 'Out of Stock' }
    ]},
    { name: 'Condition', label: 'Condition', type: 'select', options: [
      { label: 'New', value: 'New' },
      { label: 'Used', value: 'Used' }
    ]},
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
      if (data.category) formData.append('category_id', data.category);
      if (data.brand) formData.append('brand_id', data.brand);

      if (data.image instanceof File) {
        formData.append('image', data.image);
      }

      await api.patch(`products/${productId}/`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
      });

      alert('Product Updated Successfully!');

    } catch (error) {
      console.log(error.response?.data || error.message);
      alert('Failed to Update Product');
    }
  };

  return (
    <DynamicForm
      title="Edit Product"
      fields={productFields}
      onSubmit={handleProductSubmit}
      initialValues={initialValues}
    />
  );
};

export default EditProduct;