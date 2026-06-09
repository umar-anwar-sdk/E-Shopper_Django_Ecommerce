import React, { useEffect, useState } from "react";
import axios from "axios";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const AddProduct = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);

  useEffect(() => {
    fetchCategories();
    fetchBrands();
  }, []);

  const getToken = () => {
    return localStorage.getItem("accessToken");
  };

  const fetchCategories = async () => {
    try {
      const res = await axios.get(
        "https://umaranwar.pythonanywhere.com/api/categories/"
      );

      setCategories(
        res.data.map((item) => ({
          label: item.name,
          value: item.id,
        }))
      );
    } catch (error) {
      console.error(error);
    }
  };

  const fetchBrands = async () => {
    try {
      const res = await axios.get(
        "https://umaranwar.pythonanywhere.com/api/brands/"
      );

      setBrands(
        res.data.map((item) => ({
          label: item.name,
          value: item.id,
        }))
      );
    } catch (error) {
      console.error(error);
    }
  };

  const productFields = [
    {
      name: "name",
      label: "Product Name",
      type: "text",
    },
    {
      name: "price",
      label: "Product Price",
      type: "number",
    },
    {
      name: "Availability",
      label: "Availability",
      type: "select",
      options: [
        { label: "In Stock", value: "In Stock" },
        { label: "Out of Stock", value: "Out of Stock" },
      ],
    },
    {
      name: "Condition",
      label: "Condition",
      type: "select",
      options: [
        { label: "New", value: "New" },
        { label: "Used", value: "Used" },
      ],
    },
    {
      name: "category",
      label: "Category",
      type: "select",
      options: categories,
    },
    {
      name: "brand",
      label: "Brand",
      type: "select",
      options: brands,
    },
    {
      name: "image",
      label: "Product Image",
      type: "file",
    },
    {
      name: "details",
      label: "Product Details",
      type: "textarea",
    }
  ];

  const handleProductSubmit = async (data) => {
    try {
      const token = getToken();

      const formData = new FormData();

      formData.append("name", data.name);
      formData.append("price", data.price);
      formData.append("details", data.details);

      formData.append("Availability", data.Availability);

      formData.append("Condition", data.Condition);
      formData.append("category_id", data.category);
      console.log("Selected Category ID:", data.category);
      formData.append("brand_id", data.brand);
      console.log("Selected Brand ID:", data.brand);

      if (data.image) {
        formData.append("image", data.image);
      }
      const response = await axios.post(
        "https://umaranwar.pythonanywhere.com/api/products/",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log(response.data);
      alert("Product Added Successfully!");
    } catch (error) {
      console.log(error.response?.data);
      alert("Failed to Add Product");
    }
  };
  // delete method
  const handleProductDelete = async (id) => {
  const confirmDelete = window.confirm("Are you sure?");

  if (!confirmDelete) return;

  try {
    const token = localStorage.getItem("accessToken");

    await axios.delete(
      `https://umaranwar.pythonanywhere.com/api/products/${id}/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    // UI update
    setProducts((prev) => prev.filter((item) => item.id !== id));

  } catch (error) {
    console.log(error.response?.data);
  }
};

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Add Product"
        fields={productFields}
        onSubmit={handleProductSubmit}
        onDelete={handleProductDelete}
      />
    </div>
  );
};

export default AddProduct;