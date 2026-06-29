import React, { useState, useEffect } from "react";
import api from "../../services/api";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const EditCategory = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const location = useLocation();

  const [initialValues, setInitialValues] = useState({
    name: "",
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (location.state) {
      setInitialValues({ name: location.state.name });
    } else {
      fetchCategory();
    }
  }, []);

  const fetchCategory = async () => {
    try {
      const res = await api.get(`categories/${id}/`);
      setInitialValues({ name: res.data.name });
    } catch (err) {
      console.log("Fetch error:", err);
    }
  };

  const categoryFields = [
    {
      name: "name",
      label: "Category Name",
      type: "text",
      required: true,
    },
  ];

  const handleUpdate = async (formData) => {
    setLoading(true);

    try {
      await api.patch(`categories/${id}/`, formData);

      alert("Category updated successfully ✅");
      navigate("/admin/dashboard/categories");

    } catch (error) {
      console.log("Update error:", error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Edit Category"
        fields={categoryFields}
        initialValues={initialValues}
        onSubmit={handleUpdate}
        loading={loading}
      />
    </div>
  );
};

export default EditCategory;