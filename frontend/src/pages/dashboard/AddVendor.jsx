import React from 'react';
import DynamicForm from '../../components/common/admincommon/DynamicForm';
import { vendorService } from '../../services/vendorService';
import { useNavigate } from 'react-router-dom';

const AddVendor = () => {
  const navigate = useNavigate();

  const fields = [
    { name: 'first_name', label: 'First Name', type: 'text' },
    { name: 'last_name', label: 'Last Name', type: 'text' },
    { name: 'email', label: 'Email', type: 'email' },
    { name: 'phone_number', label: 'Phone Number', type: 'text' },
    { name: 'password', label: 'Password', type: 'password' },
    { name: 'company_name', label: 'Company Name', type: 'text' },
    { name: 'address', label: 'Address', type: 'textarea' },
    { name: 'status', label: 'Status', type: 'select', options: [{ label: 'active', value: 'active' }, { label: 'inactive', value: 'inactive' }] },
  ];

  const handleSubmit = async (data) => {
    try {
      await vendorService.create(data);
      alert('Vendor created');
      navigate('/admin/dashboard/vendors');
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert('Failed to create vendor');
    }
  };

  return (
    <div>
      <DynamicForm title="Add Vendor" fields={fields} onSubmit={handleSubmit} />
    </div>
  );
};

export default AddVendor;
