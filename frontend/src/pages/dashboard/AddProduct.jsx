import React, { useEffect, useState } from "react";
import axios from "axios";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const AddProduct = () => {
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
      name: "details",
      label: "Product Details",
      type: "text",
    },
    {
      name: "Availability",
      label: "Availability",
      type: "select",
      options: [
        { label: "In Stock", value: "in_stock" },
        { label: "Out of Stock", value: "out_of_stock" },
      ],
    },
    {
      name: "Condition",
      label: "Condition",
      type: "select",
      options: [
        { label: "New", value: "new" },
        { label: "Used", value: "used" },
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
  ];

  const handleProductSubmit = async (data) => {
    try {
      const token = getToken();

      const formData = new FormData();

      formData.append("name", data.name);
      formData.append("price", data.price);
      formData.append("details", data.details);

      formData.append("Availability", data.Availability.value);
      formData.append("Condition", data.Condition.value);

      formData.append("category", data.category.value);
      formData.append("brand", data.brand.value);

      if (data.image && data.image[0]) {
        formData.append("image", data.image[0]);
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

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Add Product"
        fields={productFields}
        onSubmit={handleProductSubmit}
      />
    </div>
  );
};

export default AddProduct;