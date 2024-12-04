async function getStockData() {
    const symbol = document.getElementById("symbol").value;
    if (!symbol) return alert("Please enter a stock symbol.");

    const res = await fetch(`/stocks/${symbol}`);
    const stock = await res.json();

    const stockResults = document.getElementById("stock-results");
    stockResults.innerHTML = `
        <div class="stock-item">
            <h3>${stock.symbol} - ${stock.date}</h3>
            <p>Open: ${stock.open}</p>
            <p>High: ${stock.high}</p>
            <p>Low: ${stock.low}</p>
            <p>Close: ${stock.close}</p>
            <p>Volume: ${stock.volume}</p>
        </div>
    `;
}

async function filterStocks() {
    const stockInput = document.getElementById("stock-input").value;
    if (!stockInput) return alert("Please enter stock symbols.");

    const symbols = stockInput.split(',').map(s => s.trim());
    if (symbols.length === 0) return alert("Please provide at least one stock symbol.");

    const minPrice = document.getElementById("min-price").value;
    const maxPrice = document.getElementById("max-price").value;
    const minVolume = document.getElementById("min-volume").value;
    const maxVolume = document.getElementById("max-volume").value;

    const filterData = {
        min_price: minPrice ? parseFloat(minPrice) : null,
        max_price: maxPrice ? parseFloat(maxPrice) : null,
        min_volume: minVolume ? parseInt(minVolume) : null,
        max_volume: maxVolume ? parseInt(maxVolume) : null
    };

    try {
        const res = await fetch(`/stocks/filter?symbols=${symbols.join(',')}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(filterData),
        });

        const filteredStocks = await res.json();

        const stockResults = document.getElementById("stock-results");
        stockResults.innerHTML = '';

        if (filteredStocks.length === 0) {
            stockResults.innerHTML = `<p>No stocks matched the criteria.</p>`;
        } else {
            filteredStocks.forEach(stock => {
                stockResults.innerHTML += `
                    <div class="stock-item">
                        <h3>${stock.symbol} - ${stock.date}</h3>
                        <p>Open: ${stock.open}</p>
                        <p>High: ${stock.high}</p>
                        <p>Low: ${stock.low}</p>
                        <p>Close: ${stock.close}</p>
                        <p>Volume: ${stock.volume}</p>
                    </div>
                `;
            });
        }
    } catch (error) {
        console.error("Error fetching filtered stocks:", error);
        alert("An error occurred while fetching the stocks.");
    }
}
