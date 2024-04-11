document.addEventListener('DOMContentLoaded', async () => {
    await listMesas();
});

const listMesas = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/listMesas/');
        const data = await response.json();

        // Selecciona el contenedor donde se mostrarán las tarjetas de mesa
        const mesasContainer = document.getElementById('mesasContainer');

        // Recorre los datos de las mesas y crea una tarjeta para cada una
        data.mesa.forEach(mesa => {
            // Crea un elemento de div para la tarjeta de la mesa
            const cardDiv = document.createElement('div');
            cardDiv.classList.add('col-md-4');

            // Crea el contenido HTML de la tarjeta
            cardDiv.innerHTML = `
            <div class="card mt-2">
            <div class="card-body d-flex flex-column">
                <h5 class="card-title text-center mb-4">Mesa ${mesa.idMesa}</h5> <!-- Centra el título verticalmente y agrega un margen inferior -->
                <img src="/static/img/mesa.jpg" alt="Imagen de la mesa" class="card-img-top">
                <div class="d-flex justify-content-between mb-4"> <!-- Crea un contenedor flex para los botones con espacio entre ellos -->
                    <a href="#" class="btn btn-primary">Realizar pedido</a>
                    <a href="#" class="btn btn-primary">Ver pedido</a>
                </div>
            </div>
        </div>
        `;

            // Agrega la tarjeta al contenedor de las mesas
            mesasContainer.appendChild(cardDiv);
        });

    } catch (ex) {
        alert(ex);
    }
}