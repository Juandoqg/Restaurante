const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
        { orderable: false, targets: [1, 6, 7] },
        { searchable: false, targets: [1, 7] }
    ],
    pageLength: 4,
    destroy: true
};

let dataTable;
let dataTableInit = false;

const initDatatable = async () => {
    if (dataTableInit) {
        dataTable.destroy();
    }
    await listusers();

    dataTable = $('#datatable-users').DataTable(dataTableOptions);

    dataTableInit = true;
};

const listusers = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/listUsers/')
        const data = await response.json();
        console.log(data)
        let content = ``;
        let userType = '';
        let activo = '';
        data.user.forEach((user, index) => {
            if (data.user[index].is_superuser) {
                userType = 'Administrador';
            } else if (data.user[index].is_chef) {
                userType = 'Chef';
            } else {
                userType = 'Mesero';
            }

            activo = data.user[index].is_active ? 'Activo' : 'No activo';

            content += `
                <tr id="user-${user.id}">
                    <td>${user.id}</td>
                    <td>${activo == 'Activo' ? "<p style='color: green;'>Activo</p>" : "<p style='color: red;'>Activo</p>"}</td>
                    <td>${user.email}</td>
                    <td>${user.first_name}</td>
                    <td>${user.last_name}</td>
                    <td>${user.username}</td>
                    <td>${userType}</td>
                    <td>
                        <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></button>
                    
                        ${userType == 'Administrador' ?
                    "" :
                    `<button class='btn btn-sm btn-danger' onclick="deleteUser(${user.id})"><i class='fa-solid fa-trash-can'></i></button>`}
                        </td>
                </tr>`;
        });

        tableBody_users.innerHTML = content;

    } catch (ex) {
        alert(ex);
    }
}

const deleteUser = async (userId) => {
    try {
        const response = await fetch(`/deleteUser/${userId}`, {

        });

        if (response.ok) {
            $(`#user-${userId}`).remove(); // Remove the row from the table
        } else {
            throw new Error('Failed to delete user');
        }
    } catch (ex) {
        alert(ex);
    }
}


window.addEventListener('load', async () => {
    await initDatatable();
});
