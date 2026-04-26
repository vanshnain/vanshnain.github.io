import React from "react";
import data from "./data";
import { analyzeMetrics } from "./logic";
import MetricCard from "./components/MetricCard";

function App() {
  const { insights, actions } = analyzeMetrics(data);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Developer Productivity Dashboard</h1>
      <h2>Developer: {data.developer}</h2>

      {/* Metrics */}
      <div style={{ display: "flex", flexWrap: "wrap" }}>
        <MetricCard title="Cycle Time" value={data.cycleTime} unit="days" />
        <MetricCard title="Lead Time" value={data.leadTime} unit="days" />
        <MetricCard title="Bug Rate" value={data.bugRate} unit="%" />
        <MetricCard title="Deployments" value={data.deploymentFreq} unit="/week" />
      </div>

      {/* Insights */}
      <h2>Insights</h2>
      <ul>
        {insights.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>

      {/* Actions */}
      <h2>Recommended Actions</h2>
      <ul>
        {actions.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
