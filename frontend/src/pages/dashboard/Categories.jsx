import React, { useEffect, useState } from "react";
import DataTable from "../../components/common/admincommon/DataTable";
import { useNavigate } from "react-router-dom";

const Categories = () => {
  const navigate = useNavigate();
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);

  // fetch categories
  useEffect(() => {
    setLoading(true);

    fetch("https://umaranwar.pythonanywhere.com/api/categories/")
      .then((res) => res.json())
      .then((data) => {
        // console.log("API DATA:", data);
        setCategories(data); 
      })
      .catch((err) => console.log(err))
      .finally(() => setLoading(false));
  }, []);

  // delete function

  const handleDelete = async (item) => {
  if (!window.confirm("Are you sure you want to delete this category?")) return;

  try {
    await fetch(`https://umaranwar.pythonanywhere.com/api/categories/${item.id}/`, {
      method: "DELETE",
    });

    setCategories((prev) => prev.filter((cat) => cat.id !== item.id));

  } catch (error) {
    console.error("Delete failed:", error);
  }
};
// table columns
  const columns = [
    {
      header: "ID",
      accessor: "id",
    },
    {
      header: "Category Name",
      accessor: "name",
    }
  ];

  return (
    <div>
      {/* table data */}
        <DataTable
          title="Categories"
          buttonText="Add Category"
          onAdd={() => navigate("add")}
          columns={columns}
          data={categories}
          loading={loading}
          onEdit={(item) => navigate(`edit/${item.id}`, { state: item })}
          onDelete={handleDelete}
        />
    </div>
  );
};

export default Categories;