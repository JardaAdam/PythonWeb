// Document ready (wait for full DOM load)
document.addEventListener("DOMContentLoaded", function() {
    // Clear function to handle the clearing of search only when explicitly triggered
    function clearSearch(elementId) {
        console.log(`Clearing search input for ${elementId}.`);
        const searchInput = document.getElementById(elementId);

        if (searchInput) {
            // Reset the field only explicitly on clear button
            searchInput.value = '';
            searchInput.focus();

            // Manipulate history to clean query parameters
            if (window.history.pushState) {
                const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
                window.history.pushState({ path: cleanUrl }, '', cleanUrl);
                location.reload();  // Refresh to show all records
            } else {
                // Fallback method for older browsers
                location.href = window.location.href.split('?')[0];
            }
        }
    }

    // Updating the global namespace to recognize clearSearch function
    window.clearSearch = clearSearch;
});