import React, { useEffect, useState } from "react";
import DataTable from "../../components/common/admincommon/DataTable";
import { useNavigate } from "react-router-dom";

const Brands = () => {
  const navigate = useNavigate();
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);

    fetch("https://umaranwar.pythonanywhere.com/api/brands/")
      .then((res) => res.json())
      .then((data) => {
        // console.log("API DATA:", data);
        setBrands(data); 
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
      header: "Brand Name",
      accessor: "name",
    }
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
        onEdit={(item) => console.log("Edit:", item)}
        onDelete={(item) => console.log("Delete:", item)}
        />
    </div>
  );
};

export default Brands;