import React, { useEffect, useState } from "react";
import DataTable from "../../components/common/admincommon/DataTable";
import { useNavigate } from "react-router-dom";
import api from "../../services/api";

const Brands = () => {
  const navigate = useNavigate();
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchBrands();
  }, []);

  const fetchBrands = async () => {
    setLoading(true);
    try {
      const res = await api.get("brands/");
      setBrands(res.data);
    } catch (err) {
      console.log("Fetch error:", err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this brand?");
    if (!confirmDelete) return;

    try {
      await api.delete(`brands/${id}/`);

      setBrands((prev) => prev.filter((item) => item.id !== id));

    } catch (error) {
      console.log("Delete error:", error.response?.data || error.message);
    }
  };

  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Brand Name", accessor: "name" },
  ];

  return (
    <div>
      <DataTable
        title="Brands"
        buttonText="Add Brand"
        onAdd={() => navigate("add")}
        columns={columns}
        data={brands}
        loading={loading}
        onEdit={(item) => navigate(`edit/${item.id}`, { state: item })}
        onDelete={(item) => handleDelete(item.id)}
      />
    </div>
  );
};

export default Brands;