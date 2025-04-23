document.addEventListener('DOMContentLoaded', function() {
    const abonneSearch = document.getElementById('abonneSearch');
    const livreSearch = document.getElementById('livreSearch');
    const abonneSelect = document.getElementById('abonneSelect');
    const livreSelect = document.getElementById('livreSelect');

    // Fetch and update the dropdown with matching abonnés
    abonneSearch.addEventListener('input', function() {
        const searchValue = abonneSearch.value;
        fetch(`/rechercher_abonne?terme=${searchValue}`)
            .then(response => response.json())
            .then(data => {
                abonneSelect.innerHTML = '<option value="">Sélectionnez un abonné</option>';
                data.forEach(abonne => {
                    abonneSelect.innerHTML += `<option value="${abonne.id}">${abonne.nom} ${abonne.prenom}</option>`;
                });
            });
    });

    // Fetch and update the dropdown with matching livres
    livreSearch.addEventListener('input', function() {
        const searchValue = livreSearch.value;
        fetch(`/rechercher_livre?terme=${searchValue}`)
            .then(response => response.json())
            .then(data => {
                livreSelect.innerHTML = '<option value="">Sélectionnez un livre</option>';
                data.forEach(livre => {
                    livreSelect.innerHTML += `<option value="${livre.id}">${livre.titre}</option>`;
                });
            });
    });
});
