import React, { useState } from "react";
import axios from "axios";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const EditCategory = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const existingData = location.state;

  const [initialValues] = useState({
    name: existingData?.name || "",
  });

  const categoryFields = [
    {
      name: "name",
      label: "Category Name",
      type: "text",
    },
  ];

  const getToken = () => localStorage.getItem("accessToken");

  const handleUpdate = async (data) => {
    try {
      const token = getToken();

      const response = await axios.put(
        `https://umaranwar.pythonanywhere.com/api/categories/${id}/`,
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

      alert("Category Updated Successfully!");
      navigate("/categories"); // back to list
    } catch (error) {
      console.error(error.response?.data);
      alert("Update Failed");
    }
  };

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Edit Category"
        fields={categoryFields}
        initialValues={initialValues}
        onSubmit={handleUpdate}
      />
    </div>
  );
};

export default EditCategory;