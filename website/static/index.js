document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const eventList = document.querySelector('.event-list ul');

    searchInput.addEventListener('input', () => {
        const filter = searchInput.value.toLowerCase();
        const events = eventList.querySelectorAll('li');

        events.forEach(event => {
            const title = event.querySelector('h3').textContent.toLowerCase();
            if (title.includes(filter)) {
                event.style.display = '';
            } else {
                event.style.display = 'none';
            }
        });
    });
});
