function clearSearch() {
       console.log("Clearing search input.");
       const searchInput = document.getElementById('revision-search');
       if (searchInput) {
           searchInput.value = '';
           searchInput.focus();
       }

       // Reload page without any query parameters
       if (window.history.pushState) {
           const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
           window.history.pushState({path: cleanUrl}, '', cleanUrl);
           location.reload(); // Refresh the page
       } else {
           // Fallback for browsers that do not support pushState
           location.href = window.location.href.split('?')[0];
       }
   }