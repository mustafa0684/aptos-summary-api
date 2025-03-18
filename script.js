function fetchSummary() {
    let wallet = document.getElementById("walletAddress").value;
    
    if (!wallet) {
        alert("Please enter a wallet address!");
        return;
    }

    let apiUrl = `https://yourproject.onrender.com/summary?wallet=${wallet}`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            let resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "<h3>Transaction Summaries:</h3>";

            if (data.summaries) {
                data.summaries.forEach(summary => {
                    let p = document.createElement("p");
                    p.textContent = summary;
                    resultDiv.appendChild(p);
                });
            } else {
                resultDiv.innerHTML += "<p>No transactions found.</p>";
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            alert("Failed to fetch transaction summary.");
        });
}
