import React, { useEffect, useState } from "react";

const DynamicForm = ({ fields, onSubmit, title, initialValues = {} }) => {
  const [formData, setFormData] = useState(initialValues);

  // useEffect(() => {
  //   setFormData(initialValues);
  // }, [initialValues]);
  useEffect(() => {
  if (initialValues && Object.keys(initialValues).length > 0) {
    setFormData(initialValues);
  }
}, [initialValues]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;

    setFormData({
      ...formData,
      [name]: files ? files[0] : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <>
      <h1 className="text-2xl font-bold mb-4">{title}</h1>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <form onSubmit={handleSubmit}>
          <div className="grid grid-cols-12 gap-4">
            {fields.map((field, i) => (
              <div key={i} className="col-span-6">
                <label className="block mb-2 font-bold text-[#1E293B]">
                  {field.label}
                </label>

                
                {field.type === "select" ? (
                  <select
                    name={field.name}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                    className="w-full border-[#cdcdcd] border p-2 rounded focus:outline-none"
                  >
                    <option value="">Select</option>
                    {field.options?.map((opt, idx) => (
                      <option key={idx} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                ) : field.type === "textarea" ? (
                  
                  <textarea
                    name={field.name}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                    className="w-full border-[#cdcdcd] border p-2 rounded focus:outline-none"
                  />
                ) : (
                  
                  <input
                    type={field.type}
                    name={field.name}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                    className="w-full border-[#cdcdcd] border p-2 rounded focus:outline-none"
                    required
                  />
                )}
              </div>
            ))}
          </div>

          <button className="bg-[#1E293B] mt-5 cursor-pointer text-white py-2 px-4 rounded">
            Save
          </button>
        </form>
      </div>
    </>
  );
};

export default DynamicForm;