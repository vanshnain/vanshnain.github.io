export function analyzeMetrics(data) {
  const insights = [];
  const actions = [];

  // Cycle Time
  if (data.cycleTime > 5) {
    insights.push("High cycle time indicates delays in development or code reviews.");
    actions.push("Break PRs into smaller chunks and improve review turnaround time.");
  } else {
    insights.push("Cycle time is healthy, indicating efficient development flow.");
  }

  // Lead Time
  if (data.leadTime > 8) {
    insights.push("High lead time suggests slow delivery to production.");
    actions.push("Optimize CI/CD pipeline and reduce bottlenecks.");
  } else {
    insights.push("Lead time is optimal, indicating fast delivery.");
  }

  // Bug Rate
  if (data.bugRate > 10) {
    insights.push("High bug rate indicates quality issues in code.");
    actions.push("Improve testing coverage and enforce better code reviews.");
  } else {
    insights.push("Bug rate is under control.");
  }

  // Deployment Frequency
  if (data.deploymentFreq < 3) {
    insights.push("Low deployment frequency indicates infrequent releases.");
    actions.push("Adopt smaller, more frequent deployments.");
  } else {
    insights.push("Deployment frequency is good.");
  }

  return { insights, actions };
}
