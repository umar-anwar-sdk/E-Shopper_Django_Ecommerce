import React, { useEffect, useState } from 'react';
import DynamicForm from '../../components/common/admincommon/DynamicForm';
import { vendorService } from '../../services/vendorService';
import { useNavigate, useParams } from 'react-router-dom';

const EditVendor = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [initial, setInitial] = useState({});

  useEffect(() => {
    const fetchVendor = async () => {
      try {
        const res = await vendorService.get(id);
        setInitial(res.data);
      } catch (err) {
        console.log(err.response?.data || err.message);
      }
    };
    if (id) fetchVendor();
  }, [id]);

  const fields = [
    { name: 'first_name', label: 'First Name', type: 'text' },
    { name: 'last_name', label: 'Last Name', type: 'text' },
    { name: 'email', label: 'Email', type: 'email' },
    { name: 'phone_number', label: 'Phone Number', type: 'text' },
    { name: 'company_name', label: 'Company Name', type: 'text' },
    { name: 'address', label: 'Address', type: 'textarea' },
    { name: 'status', label: 'Status', type: 'select', options: [{ label: 'active', value: 'active' }, { label: 'inactive', value: 'inactive' }] },
  ];

  const handleSubmit = async (data) => {
    try {
      await vendorService.update(id, data);
      alert('Vendor updated');
      navigate('/admin/dashboard/vendors');
    } catch (err) {
      console.log(err.response?.data || err.message);
      alert('Failed to update vendor');
    }
  };

  return (
    <div>
      <DynamicForm title="Edit Vendor" fields={fields} onSubmit={handleSubmit} initialValues={initial} />
    </div>
  );
};

export default EditVendor;
