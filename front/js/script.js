document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch("/alumne/list")
        .then(response =>{
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                const cicleAluCell = document.createElement("td");
                cicleAluCell.textContent = alumne.Cicle;
                row.appendChild(cicleAluCell);

                const cursAluCell = document.createElement("td");
                cursAluCell.textContent = alumne.Curs;
                row.appendChild(cursAluCell);

                const grupAluCell = document.createElement("td");
                grupAluCell.textContent = alumne.Grup;
                row.appendChild(grupAluCell);

                const nomAulaAluCell = document.createElement("td");
                nomAulaAluCell.textContent = alumne.DescAula;
                row.appendChild(nomAulaAluCell);

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});