document.addEventListener('DOMContentLoaded', function() {
        // Získání `<select>` elementu pro výběr typu modelu
        const modelTypeSelect = document.getElementById('model_type_select');

        // Načtení předvoleného typu modelu z `<select>` elementu
        const modelType = modelTypeSelect.value;

        // Pokud existuje předvolený typ modelu, načteme příslušný formulář při spuštění stránky
        if (modelType) {
            loadForm(modelType);
        }

        // Přidání posluchače pro změny ve `<select>` elementu
        modelTypeSelect.addEventListener('change', function() {
            // Získat vybraný typ modelu
            const selectedModelType = this.value;
            // Načíst formulář odpovídající vybranému typu modelu
            loadForm(selectedModelType);
        });
    });

    // Funkce pro načítání formuláře na základě zvoleného typu modelu
    function loadForm(modelType) {
        // Získání CSRF tokenu pro bezpečné odesílání požadavků
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        // Kontejner pro načtení formuláře
        const formContainer = document.getElementById('form-container');

        // Odeslat GET požadavek pro načtení HTML formuláře pro daný typ modelu
        fetch(`/revisions/get_form/?model_type=${modelType}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => response.text())
        .then(html => {
            // Vložení získaného HTML formuláře do kontejneru
            formContainer.innerHTML = html;

            // Získání formuláře z kontejneru
            const form = formContainer.querySelector('form');

            // Pokud formulář existuje, přidání posluchače pro jeho odeslání
            if (form) {
                form.addEventListener('submit', function(event) {
                    // Zabránit standardnímu odeslání formuláře
                    event.preventDefault();

                    // Shromažďování dat z formuláře
                    const formData = new FormData(form);
                    // Odeslat POST požadavek s daty z formuláře
                    fetch(this.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-CSRFToken': csrfToken
                        }
                    })
                    .then(response => {
                        if (response.ok) {
                            // Pokud je odeslání úspěšné, zobrazit uživateli zprávu
                            alert('Data submitted successfully.');
                            form.reset(); // Reset formuláře
                            // Přesměrování zpět na aktuální URL s parametrem `model_type`, aby zůstal stejný formulář
                            window.location.href = `${window.location.pathname}?model_type=${modelType}`;
                        } else {
                            // Ošetření chybného stavu
                            console.error('Error submitting form.');
                        }
                    })
                    .catch(error => console.error('Error:', error));
                });
            }
        })
        .catch(error => console.error('Error:', error));
    }