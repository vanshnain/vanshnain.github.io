const express = require("express");
const app = express();

app.use(express.json());
app.use(require("cors")());

// Optimization logic (simple example)
function calculatePriority(data) {
  // Higher priority + closer distance + earlier deadline = better
  return (
    data.priority * 2 +
    (100 - data.distance) +
    (100 - data.deadline)
  );
}

app.post("/optimize", (req, res) => {
  const data = req.body;

  const score = calculatePriority(data);

  res.json({
    message: "Optimized Successfully",
    score: score
  });
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
