console.log("✅ script.js is successfully loaded!");

// 🔹 Function to Load Stock Availability
function loadStockData() {
    fetch("http://127.0.0.1:8000/stocks/")
    .then(response => response.json())
    .then(stockData => {
        const stockTableBody = document.getElementById("stockTableBody");
        stockTableBody.innerHTML = ""; // Clear previous data
        
        stockData.forEach(stock => {
            const row = `<tr>
                <td>${stock.id}</td>
                <td>${stock.product_name}</td>
                <td>${stock.quantity}</td>
                <td>${stock.last_updated}</td>
            </tr>`;
            stockTableBody.innerHTML += row;
        });
    })
    .catch(error => console.error("❌ Error fetching stock data:", error));
}
// 🔹 Function to Load Product Details
function loadProductsTable() {
    fetch("http://127.0.0.1:8000/products/")
        .then(response => {
            if (!response.ok) {
                throw new Error(`❌ HTTP Error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("📦 Fetched products:", data); // ✅ Debugging step

            const tableBody = document.getElementById("productsTableBody");
            if (!tableBody) {
                console.error("❌ Error: productsTableBody not found in HTML");
                return;
            }

            tableBody.innerHTML = ""; // Clear previous data
            data.forEach(product => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${product.name || "N/A"}</td>
                    <td>${product.category || "Uncategorized"}</td>
                    <td>$${(product.price || 0).toFixed(2)}</td>
                    <td>${product.stock || 0}</td>
                    <td>${product.discount_percentage || "0%"}%</td>
                    <td>${product.seller_name || "Unknown Seller"}</td>
                    <td>${product.seller_contact || "N/A"}</td>
                `;
                tableBody.appendChild(row);
            });
            console.log("✅ Product data loaded successfully!");
        })
        .catch(error => console.error("❌ Error fetching products:", error));
}

// 🔹 Ensure both functions run properly on page load
window.onload = function () {
    loadStockData();
    loadProductsTable();
};
// 🔹 Form Submission Handler
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById("addProductForm");
    if (!form) {
        console.error("❌ Error: addProductForm not found in HTML");
        return;
    }

    form.addEventListener("submit", function(e) {
        e.preventDefault();
        
        // Get form values
        const formData = {
            name: document.getElementById("product-name").value.trim(),
            category: document.getElementById("category").value.trim() || "Uncategorized",
            price: parseFloat(document.getElementById("price").value) || 0,
            stock: parseInt(document.getElementById("stock").value) || 0,
            discount_percentage: parseFloat(document.getElementById("discount").value) || 0,
            seller_name: document.getElementById("seller-name").value.trim() || "Unknown",
            seller_contact: document.getElementById("seller-contact").value.trim() || "N/A"
        };

        // Validation
        if (!formData.name) {
            alert("❌ Product name is required!");
            return;
        }

        if (formData.price < 0 || formData.stock < 0) {
            alert("❌ Price and stock must be non-negative!");
            return;
        }

        // Send data to backend
        fetch("http://127.0.0.1:8000/products/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formData)
        })
        .then(async response => {
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Failed to add product");
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Product added successfully:", data);
            alert("✅ Product added successfully!");
            form.reset();
            loadProductsTable(); // Reload the table
        })
        .catch(error => {
            console.error("❌ Error:", error);
            alert(`❌ ${error.message}`);
        });
    });
});