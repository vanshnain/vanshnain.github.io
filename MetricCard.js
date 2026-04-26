import React from "react";

function MetricCard({ title, value, unit }) {
  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "10px",
      padding: "15px",
      margin: "10px",
      width: "200px",
      boxShadow: "0 2px 5px rgba(0,0,0,0.1)"
    }}>
      <h3>{title}</h3>
      <p style={{ fontSize: "20px", fontWeight: "bold" }}>
        {value} {unit}
      </p>
    </div>
  );
}

export default MetricCard;
