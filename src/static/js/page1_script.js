document.getElementById("billForm").onsubmit = async function(event) {
    event.preventDefault();
    const units = document.getElementById("units").value;

    const response = await fetch("/calculate_billAmount", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ units: units })
    });

    const result = await response.json();
    
    if (result.df_html) {
        document.getElementById("df_html").innerHTML = result.df_html;
        document.getElementById("totalCost").innerText = `Rs.${parseFloat(result.amount).toFixed(2)}`;
    } else {
        document.getElementById("output").innerText = `Error: ${result.error}`;
    }
};