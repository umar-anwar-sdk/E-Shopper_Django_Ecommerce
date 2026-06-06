import React from "react";
import axios from "axios";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const AddBrand = () => {
  const brandFields = [
    {
      name: "name",
      label: "Brand Name",
      type: "text",
    },
  ];

  const getToken = () => {
    return localStorage.getItem("accessToken");
  };

  const handleBrandSubmit = async (data) => {
    try {
      const token = getToken();

      const response = await axios.post(
        "https://umaranwar.pythonanywhere.com/api/brands/",
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
      alert("Brand Added Successfully!");
    } catch (error) {
      console.error(error.response?.data);
      alert("Failed to Add Brand");
    }
  };
  const token = localStorage.getItem("refreshToken");
console.log("Token:", token);

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Add Brand"
        fields={brandFields}
        onSubmit={handleBrandSubmit}
      />
    </div>
  );
};

export default AddBrand;