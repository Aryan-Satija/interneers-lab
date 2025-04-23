const container = document.getElementById("product-container")

async function getProducts(){
    container.innerHTML = "";

    const spinner = document.createElement("div");
    spinner.className = "spinner"
    container.appendChild(spinner)

    try{
        const response = await fetch("http://localhost:8000/api/v1/product?page_size=-5")
        
        if(!response.ok){
            throw new Error("Failed to fetch products: " + response.statusText);
        }

        const data = await response.json();
        
        spinner.remove()

        data.products.forEach((product) => {
            const tile = document.createElement("div");
            tile.className = "product-tile"
            
            tile.innerHTML = `
                <h2>${product.name}</h2>
                <p>${product.description}</p>
                <p><strong>Price: </strong>${product.price}</p>
                <p><strong>Quantity: </strong>${product.quantity}</p>
                <p><strong>Brand: </strong>${product.brand}</p>
                <p><strong>Category: </strong>${product.category}</p>
            `

            container.appendChild(tile);
        })

    } catch(err){
        console.log(err)
        container.innerHTML = `<p>Failed to load products. Please try again later!</p>`
    }
}

getProducts();
