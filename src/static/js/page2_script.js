document.getElementById("unitsForm").onsubmit = async function(event) {
    event.preventDefault();
    const billAmount = document.getElementById("billAmount").value;

    const response = await fetch("/determine_unitsConsumed", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ billAmount: billAmount })
    });

    const result = await response.json();
    
    if (result.unitsConsumed) {
        document.getElementById("unitsConsumed").innerText = `${result.unitsConsumed} units consumed`;
    } else {
        document.getElementById("unitsConsumed").innerText = `Error: ${result.error}`;
    }
};