import React, { useEffect, useState } from 'react';
import api from '../../services/api';

const VendorProfile = () => {
  const [profile, setProfile] = useState(null);
  const userId = localStorage.getItem('userId');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const res = await api.get(`vendors/${userId}/`);
        setProfile(res.data);
      } catch (err) {
        console.log(err.response?.data || err.message);
      }
    };
    if (userId) fetchProfile();
  }, [userId]);

  if (!profile) return <div>Loading...</div>;

  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-semibold mb-4">Profile</h2>
      <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
      <p><strong>Company:</strong> {profile.company_name}</p>
      <p><strong>Email:</strong> {profile.email}</p>
      <p><strong>Phone:</strong> {profile.phone_number}</p>
      <p><strong>Address:</strong> {profile.address}</p>
      <p><strong>Status:</strong> {profile.status}</p>
    </div>
  );
};

export default VendorProfile;
