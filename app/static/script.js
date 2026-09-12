document.getElementById("calculate-btn").addEventListener("click", async () => {
  const a = parseFloat(document.getElementById("a").value);
  const b = parseFloat(document.getElementById("b").value);
  const operation = document.getElementById("operation").value;
  const resultDiv = document.getElementById("result");

  try {
    const response = await fetch("/api/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ operation, a, b }),
    });
    const data = await response.json();
    if (!response.ok) {
      resultDiv.textContent = `Error: ${data.error}`;
      return;
    }
    resultDiv.textContent = `Result: ${data.result}`;
  } catch (err) {
    resultDiv.textContent = "Error: could not reach the server.";
  }
});