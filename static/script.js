document.addEventListener("DOMContentLoaded", function () {
    const tableBody = document.querySelector("#vacacionesTable tbody");
    const diasHeader = document.getElementById("diasHeader");

    let data = [];
    let sortAsc = true;

    function loadCSV() {
        fetch("/vacacion.csv")
            .then((res) => res.text())
            .then((csv) => {
                const rows = csv.trim().split("\n").slice(1); // quitar cabecera
                data = rows.map(row => {
                    const [Periodo, Nombre, Dni, Cargo, Ingreso, Vacaciones, Estado, Dias] = row.split(",");
                    return { Periodo, Nombre, Dni, Cargo, Ingreso, Vacaciones, Estado, Dias: parseInt(Dias) || 0 };
                });
                renderTable(data);
            });
    }

    function renderTable(filteredData) {
        tableBody.innerHTML = "";
        filteredData.forEach(row => {
            const tr = document.createElement("tr");
            tr.innerHTML = `
                <td>${row.Periodo}</td>
                <td>${row.Nombre}</td>
                <td>${row.Dni}</td>
                <td>${row.Cargo}</td>
                <td>${row.Ingreso}</td>
                <td>${row.Vacaciones}</td>
                <td>${row.Estado}</td>
                <td>${row.Dias}</td>
            `;
            tableBody.appendChild(tr);
        });
    }

    function filterData() {
        const periodo = document.getElementById("filterPeriodo").value.toLowerCase();
        const nombre = document.getElementById("filterNombre").value.toLowerCase();
        const cargo = document.getElementById("filterCargo").value.toLowerCase();
        const dias = document.getElementById("filterDias").value;

        const filtered = data.filter(row =>
            row.Periodo.toLowerCase().includes(periodo) &&
            row.Nombre.toLowerCase().includes(nombre) &&
            row.Cargo.toLowerCase().includes(cargo) &&
            (dias === "" || row.Dias === parseInt(dias))
        );

        renderTable(filtered);
    }

    document.getElementById("filterPeriodo").addEventListener("input", filterData);
    document.getElementById("filterNombre").addEventListener("input", filterData);
    document.getElementById("filterCargo").addEventListener("input", filterData);
    document.getElementById("filterDias").addEventListener("input", filterData);

    diasHeader.addEventListener("click", function () {
        sortAsc = !sortAsc;
        data.sort((a, b) => sortAsc ? a.Dias - b.Dias : b.Dias - a.Dias);
        filterData();
    });

    loadCSV();
});
