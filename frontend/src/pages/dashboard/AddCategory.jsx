import React from "react";
import axios from "axios";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const AddCategory = () => {
  const categoryFields = [
    {
      name: "name",
      label: "Category Name",
      type: "text",
    },
  ];

  const getToken = () => {
    return localStorage.getItem("accessToken");
  };

  const handleCategorySubmit = async (data) => {
    try {
      const token = getToken();

      const response = await axios.post(
        "https://umaranwar.pythonanywhere.com/api/categories/",
        {
          name: data.name,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response.data);
      alert("Category Added Successfully!");
    } catch (error) {
      console.error(error.response?.data);
      alert("Failed to Add Category");
    }
  };
  const token = localStorage.getItem("refreshToken");
console.log("Token:", token);

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Add Category"
        fields={categoryFields}
        onSubmit={handleCategorySubmit}
      />
    </div>
  );
};

export default AddCategory;