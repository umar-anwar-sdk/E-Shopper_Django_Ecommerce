import React, { useEffect, useState } from 'react';
import DataTable from '../../components/common/admincommon/DataTable';
import { useNavigate } from 'react-router-dom';
import { vendorService } from '../../services/vendorService';

const Vendors = () => {
  const navigate = useNavigate();
  const [vendors, setVendors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchVendors();
  }, []);

  const fetchVendors = async (q) => {
  setLoading(true);
  try {
    const res = await vendorService.list(q ? { search: q } : {});
    setVendors(res.data.vendors); 
  } catch (err) {
    console.log(err.response?.data || err.message);
  } finally {
    setLoading(false);
  }
};

  const handleDelete = async (item) => {
    if (!window.confirm('Delete this vendor?')) return;
    try {
      await vendorService.remove(item.id);
      setVendors((prev) => prev.filter((v) => v.id !== item.id));
    } catch (err) {
      console.log(err.response?.data || err.message);
    }
  };

  const columns = [
  { header: 'ID', accessor: 'id' },
  { header: 'Name', render: (row) => `${row.first_name} ${row.last_name}` },
  { header: 'Email', accessor: 'email' },
  { header: 'Phone', render: (row) => row.phone_number || '-' },
{ header: 'Shop', render: (row) => row.shop_name || '-' },
  {
    header: 'Status',
    render: (row) => (row.is_verified ? 'Verified' : 'Not Verified'),
  },
];

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-3xl font-bold">Vendors</h2>
        <div className="flex gap-2">
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search vendors" className="border p-2 rounded" />
          <button onClick={() => fetchVendors(search)} className="px-3 py-2 bg-gray-800 text-white rounded">Search</button>
          <button onClick={() => navigate('/vendor/dashboard/add-product')} className="px-3 py-2 bg-blue-600 text-white rounded">Add Vendor</button>
        </div>
      </div>

      <DataTable
        columns={columns}
        data={vendors}
        loading={loading}
        onEdit={(item) => navigate(`/admin/dashboard/vendors/edit/${item.id}`)}
        onDelete={(item) => handleDelete(item)}
      />
    </div>
  );
};

export default Vendors;
