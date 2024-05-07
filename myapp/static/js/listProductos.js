document.addEventListener('DOMContentLoaded', async () => {
    await listProductos();
});

const pedido = [];

const listProductos = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/listProductos/');
        const listProducts = await response.json();
        console.log(listProducts)
        


        const productosContainer = document.getElementById('productosContainer');

        listProducts.producto.forEach(producto => {
            const cardDiv = document.createElement('div');
            cardDiv.classList.add('col-md-4');

            // Determinar la clase CSS para el botón de "Pedir" según la disponibilidad del producto
            const disponible = producto.disponible ? 'Disponible' : 'No disponible';
            const colorTexto = producto.disponible ? 'green' : 'red';

            cardDiv.innerHTML = `
                <div class="card mt-2">
                    <div class="card-header d-flex justify-content-center align-items-center">
                        <img src="/static/${producto.imgProducto}" alt="Imagen del producto" class="card-img-top">
                    </div>
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title text-center mb-4">Producto:  ${producto.nombre}</h5>
                        <h5 class="card-title text-center mb-4">Precio:  ${producto.precio}</h5>
                        <h5 class="card-title text-center mb-4">Disponible:  ${producto.disponible}</h5>
                        <h5 class="card-title text-center mb-4">Descripción:  ${producto.descripcion}</h5>
                        <div id="disponible" style="color: ${colorTexto};">${disponible}</div>
                        <div class="form-group mt-3">
                            <label for="cantidad-${producto.idProducto}">Cantidad:</label>
                            <input type="number" id="cantidad-${producto.idProducto}" class="form-control" value="1" min="1">
                        </div>
                        <button class="btn btn-primary mt-3" onclick="agregarAlPedido(${producto.idProducto})">Pedir</button>
                    </div>
                </div>
            `;
            productosContainer.appendChild(cardDiv);
        });

    } catch (ex) {
        alert(ex);
    }
}

function agregarAlPedido(idProducto) {
    const cantidadInput = document.getElementById(`cantidad-${idProducto}`);
    console.log("Cantidad input:", cantidadInput); // Agregar este log para verificar si se encuentra el elemento
    const cantidad = parseInt(cantidadInput.value);
    pedido.push({ id: idProducto, cantidad: cantidad });
    console.log("Producto agregado al pedido:", idProducto, "Cantidad:", cantidad);
    console.log(pedido)
}

