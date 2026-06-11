import React, { useState, useEffect } from "react";
import api from "../../services/api";
import { useLocation, useParams, useNavigate } from "react-router-dom";
import DynamicForm from "../../components/common/admincommon/DynamicForm";

const EditBrands = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const location = useLocation();

  const [initialValues, setInitialValues] = useState({
    name: "",
  });

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (location.state && location.state.name) {
      setInitialValues({ name: location.state.name });
    } else {
      fetchBrand();
    }
  }, [id]);

  const fetchBrand = async () => {
    try {
      const res = await api.get(`brands/${id}/`);
      setInitialValues({ name: res.data.name });
    } catch (err) {
      console.log("Fetch error:", err);
    }
  };

  const brandFields = [
    {
      name: "name",
      label: "Brand Name",
      type: "text",
      required: true,
    },
  ];

  const handleUpdate = async (formData) => {
    setLoading(true);
    try {
      await api.patch(`brands/${id}/`, formData);

      alert("Brand updated successfully ✅");
      navigate("/admin/dashboard/brands");
    } catch (error) {
      console.log("Update error:", error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-5">
      <DynamicForm
        title="Edit Brand"
        fields={brandFields}
        initialValues={initialValues}
        onSubmit={handleUpdate}
      />
    </div>
  );
};

export default EditBrands;