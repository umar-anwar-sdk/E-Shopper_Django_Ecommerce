import React, { useEffect, useState } from 'react';
import { vendorService } from '../../services/vendorService';
import { useParams } from 'react-router-dom';

const VendorDetails = () => {
  const { id } = useParams();
  const [vendor, setVendor] = useState(null);

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await vendorService.get(id);
        setVendor(res.data);
      } catch (err) {
        console.log(err.response?.data || err.message);
      }
    };
    if (id) fetch();
  }, [id]);

  if (!vendor) return <div>Loading...</div>;

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Vendor Details</h2>
      <p><strong>Name:</strong> {vendor.first_name} {vendor.last_name}</p>
      <p><strong>Company:</strong> {vendor.company_name}</p>
      <p><strong>Email:</strong> {vendor.email}</p>
      <p><strong>Phone:</strong> {vendor.phone_number}</p>
      <p><strong>Address:</strong> {vendor.address}</p>
      <p><strong>Status:</strong> {vendor.status}</p>
      <p><strong>Products:</strong> {vendor.products_count ?? 0}</p>
    </div>
  );
};

export default VendorDetails;
