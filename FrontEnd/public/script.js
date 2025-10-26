async function predict() {
  const featuresText = document.getElementById("features").value.trim();
  if (!featuresText) {
    alert("Please enter the feature list!");
    return;
  }

  const features = featuresText.split(",").map(Number);

  const response = await fetch("https://fraud-api.vercel.app/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ features })
  });

  const result = await response.json();
  document.getElementById("result").innerHTML = `
    <p><b>Prediction:</b> ${result.result}</p>
    <p><b>Probability:</b> ${result.probability.toFixed(4)}</p>
  `;
}
