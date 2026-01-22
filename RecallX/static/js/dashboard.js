/**
 * Dashboard JavaScript
 * Handles topic display and user interactions on dashboard
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    loadTopics();
});

function loadTopics() {
    fetch('/api/topics')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Dashboard already renders topics from backend
                console.log('Topics loaded:', data.topics);
            }
        })
        .catch(error => console.error('Error loading topics:', error));
}

// Add smooth transitions
document.addEventListener('DOMContentLoaded', function() {
    // Animate topic cards on load
    const cards = document.querySelectorAll('.topic-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(10px)';
        setTimeout(() => {
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
});
