import React from "react";
import { HiOutlinePencilAlt } from "react-icons/hi";
import { RiDeleteBin5Line } from "react-icons/ri";
const DataTable = ({
  title,
  buttonText,
  onAdd,
  columns = [],
  data = [],
  loading = false,
  onEdit,
  onDelete,
}) => {
  return (
    <div className="container mx-auto px-4 my-10">
        {/* HEADER SECTION */}
      {(title || onAdd) && (
        <div className="flex justify-between items-center mb-4">

          {/* TITLE */}
          {title && (
            <h2 className="text-3xl font-bold text-gray-800">
              {title}
            </h2>
          )}

          {/* ADD BUTTON */}
          {onAdd && (
            <button
              onClick={onAdd}
              className="px-4 py-2 cursor-pointer bg-gray-800 text-white rounded-lg hover:bg-gray-600"
            >
              {buttonText || "Add"}
            </button>
          )}

        </div>
      )}
    <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white">
      <table className="w-full text-left">

        {/* HEAD */}
        <thead className="bg-gray-100 shadow-lg">
          <tr>
            {columns.map((col, index) => (
              <th
                key={index}
                className="px-4 py-3 font-semibold text-gray-700"
              >
                {col.header}
              </th>
            ))}

            {/* Action Column */}
            {(onEdit || onDelete) && (
              <th className="px-4 py-3 font-semibold text-gray-700">
                Actions
              </th>
            )}
          </tr>
        </thead>

        {/* BODY */}
        <tbody>
          {loading ? (
            <tr>
              <td
                colSpan={columns.length + 1}
                className="text-center py-5"
              >
                <div className="flex items-center justify-center">
                    <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                </div>
              </td>
            </tr>
          ) : data.length > 0 ? (
            data.map((item, rowIndex) => (
              <tr
                key={rowIndex}
                className="border-t border-gray-200 hover:bg-gray-50"
              >
                {columns.map((col, colIndex) => (
                  <td key={colIndex} className="px-4 py-3">
                    {col.render
                      ? col.render(item)
                      : item[col.accessor]}
                  </td>
                ))}

                {/* ACTION BUTTONS */}
                {(onEdit || onDelete) && (
                  <td className="px-4 py-3 flex items-center gap-2">
                    
                    {onEdit && (
                      <button
                        onClick={() => onEdit(item)}
                        className="text-2xl text-blue-500 hover:text-blue-700 cursor-pointer">
                        <HiOutlinePencilAlt />
                      </button>
                    )}

                    {onDelete && (
                      <button
                        onClick={() => onDelete(item.id)}
                        className="text-2xl text-red-500 hover:text-red-700 cursor-pointer">
                        <RiDeleteBin5Line />
                      </button>
                    )}

                  </td>
                )}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length + 1}
                className="text-center py-5"
              >
                No Data Found
              </td>
            </tr>
          )}
        </tbody>

      </table>
        </div>
    </div>
  );
};

export default DataTable;