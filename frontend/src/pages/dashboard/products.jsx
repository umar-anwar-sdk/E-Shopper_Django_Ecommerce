import React, { useEffect, useState } from "react";
import DataTable from "../../components/common/admincommon/DataTable";
import { useNavigate } from "react-router-dom";

const Products = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    fetch("https://umaranwar.pythonanywhere.com/api/products/")
      .then((res) => res.json())
      .then((data) => {
        // console.log("API DATA:", data);
        setProducts(data); 
      })
      .catch((err) => console.log(err))
      .finally(() => setLoading(false));
  }, []);

  const columns = [
    {
      header: "ID",
      accessor: "id",
    },
    {
      header: "Product Name",
      accessor: "name",
    },
    {
      header: "Price",
      render: (row) => `Rs ${row.price}`,
    },
    {
      header: "Category",
      accessor: "category",
    },
    {
      header: "Brand",
      accessor: "brand",
    },
    {
      header: "Stock Status",
      accessor: "Availability",
    },
    {
      header: "Condition",
      accessor: "Condition",
    },
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
            onDelete={(item) => console.log("Delete:", item)}
        />
    </div>
  );
};

export default Products;