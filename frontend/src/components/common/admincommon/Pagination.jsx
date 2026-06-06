import React from "react";

const Pagination = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  return (
    <div
      style={{
        display: "flex",
        gap: "10px",
        justifyContent: "center",
        marginTop: "20px",
      }}
    >
      <button
        disabled={currentPage === 1}
        onClick={() => onPageChange(currentPage - 1)}
      >
        Prev
      </button>

      <span>
        {currentPage} / {totalPages}
      </span>

      <button
        disabled={currentPage === totalPages}
        onClick={() => onPageChange(currentPage + 1)}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;