import React, { useEffect, useState } from "react";

const DynamicForm = ({ fields, onSubmit, title, initialValues = {} }) => {
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState(initialValues);

  useEffect(() => {
    if (initialValues && Object.keys(initialValues).length > 0) {
      setFormData(initialValues);
    }
  }, [initialValues]);

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: type === "file" ? files[0] : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await onSubmit(formData);
      setFormData({});
      e.target.reset(); // 👈 important for file input reset
    } finally {
      setLoading(false);
    }
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

                {/* SELECT */}
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

                /* TEXTAREA */
                ) : field.type === "textarea" ? (
                  <textarea
                    name={field.name}
                    value={formData[field.name] || ""}
                    onChange={handleChange}
                    className="w-full border-[#cdcdcd] border p-2 rounded focus:outline-none"
                  />

                /* FILE INPUT (FIXED) */
                ) : field.type === "file" ? (
                  <input
                    type="file"
                    name={field.name}
                    onChange={handleChange}
                    className="w-full border-[#cdcdcd] border p-2 rounded focus:outline-none"
                  />

                /* NORMAL INPUT */
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

          <button
            disabled={loading}
            className={`mt-5 text-white py-2 px-4 rounded ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-[#1E293B]"
            }`}
          >
            {loading ? "Saving..." : "Save"}
          </button>
        </form>
      </div>
    </>
  );
};

export default DynamicForm;