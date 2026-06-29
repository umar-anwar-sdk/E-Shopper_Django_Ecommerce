import React, { useEffect, useState } from 'react';
import api from '../../services/api';

const VendorDashboard = () => {
  const [stats, setStats] = useState({});
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // attempt to fetch vendor stats; endpoints may vary
        const res = await api.get(`vendors/${userId}/stats/`);
        setStats(res.data);
      } catch (err) {
        // fallback: fetch products count
        try {
          const prodRes = await api.get(`products/?vendor_id=${userId}`);
          setStats({ total_products: prodRes.data.length });
        } catch (e) {
          // ignore
        }
      }
    };

    if (userId) fetchStats();
  }, [userId]);

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div className="bg-white p-4 rounded shadow"> 
        <h3 className="font-semibold">Total Products</h3>
        <p className="text-2xl">{stats.total_products ?? 0}</p>
      </div>

      <div className="bg-white p-4 rounded shadow"> 
        <h3 className="font-semibold">Active Products</h3>
        <p className="text-2xl">{stats.active_products ?? 0}</p>
      </div>

      <div className="bg-white p-4 rounded shadow"> 
        <h3 className="font-semibold">Inactive Products</h3>
        <p className="text-2xl">{stats.inactive_products ?? 0}</p>
      </div>

      <div className="bg-white p-4 rounded shadow"> 
        <h3 className="font-semibold">Total Sales</h3>
        <p className="text-2xl">{stats.total_sales ?? 0}</p>
      </div>
    </div>
  );
};

export default VendorDashboard;
