import React, { useEffect, useState } from "react";
import DataTable from "../../components/common/admincommon/DataTable";
import { useNavigate } from "react-router-dom";
import api from "../../services/api"; 

const Products = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await api.get("products/");
      setProducts(res.data);
    } catch (err) {
      console.log("Fetch error:", err.response?.data || err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this product?");
    if (!confirmDelete) return;

    try {
      await api.delete(`products/${id}/`);

      setProducts((prev) => prev.filter((item) => item.id !== id));

    } catch (error) {
      console.log("Delete error:", error.response?.data || error.message);
    }
  };

  const columns = [
    { header: "ID", accessor: "id" },
    { header: "Product Name", accessor: "name" },
    { header: "Price", render: (row) => `Rs ${row.price}` },
    { header: "Category", accessor: "category" },
    { header: "Brand", accessor: "brand" },
    { header: "Stock Status", accessor: "Availability" },
    { header: "Condition", accessor: "Condition" },
    {
      header: "Image",
      render: (row) => (
        <img
          src={row.image}
          alt={row.name}
          style={{ width: "50px", height: "50px", objectFit: "cover" }}
        />
      ),
    },
  ];

  return (
    <div>
      <DataTable
        title="Products"
        buttonText="Add Product"
        onAdd={() => navigate("add")}
        columns={columns}
        data={products}
        loading={loading}
        onEdit={(item) => console.log("Edit:", item)}
        onDelete={(item) => handleDelete(item.id)}
      />
    </div>
  );
};

export default Products;