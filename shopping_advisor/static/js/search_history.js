// Function to save search history
function saveSearchHistory(searchTerm) {
    let history = JSON.parse(localStorage.getItem('searchHistory')) || [];

    if (!history.includes(searchTerm)) {
        history.push(searchTerm);
        localStorage.setItem('searchHistory', JSON.stringify(history));
    }
}

// Function to clear cached results
function clearCachedResults() {
    localStorage.removeItem('searchCache');
}

// Event listener for form submission
document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior

    const searchTerm = document.getElementById('searchTerm').value.trim();

    // Save search history
    saveSearchHistory(searchTerm);

    // Implement your search logic here
    // For example, you might make an AJAX call to fetch search results
    // and then display them using displayResults(results);
});
