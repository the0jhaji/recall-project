/**
 * Search & Topic Creation JavaScript
 * Handles topic creation and AI-powered internet search
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addTopicForm');
    if (form) {
        form.addEventListener('submit', handleAddTopic);
    }
});

function handleAddTopic(e) {
    e.preventDefault();

    const subject = document.getElementById('subject').value;
    const topic_name = document.getElementById('topic_name').value;
    const exam_type = document.getElementById('exam_type').value;
    const description = document.getElementById('description').value;

    showLoading('Creating topic and searching internet...');

    // First, create the topic
    fetch('/api/add-topic', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            subject: subject,
            topic_name: topic_name,
            exam_type: exam_type,
            description: description
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const topic_id = data.topic_id;
            
            // Now search the internet for the topic
            return fetch('/api/search-topic', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic_id: topic_id,
                    topic_name: topic_name,
                    search_query: `${topic_name} ${exam_type} exam questions`
                })
            });
        } else {
            throw new Error(data.error || 'Failed to create topic');
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess(`✅ Topic "${data.topic_id}" created successfully!\n\nInternet Search Results:\n${data.questions_generated} questions generated from ${data.search_results.length} sources`);
        } else {
            showError(data.error || 'Failed to search internet');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showError('Error: ' + error.message);
    });
}

function showLoading(message = 'Processing...') {
    document.getElementById('loadingMessage').style.display = 'block';
    document.getElementById('loadingMessage').querySelector('p').textContent = message;
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('addTopicForm').style.display = 'none';
}

function showSuccess(message) {
    document.getElementById('loadingMessage').style.display = 'none';
    document.getElementById('successMessage').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('successText').textContent = message;
    document.getElementById('addTopicForm').style.display = 'none';
}

function showError(message) {
    document.getElementById('loadingMessage').style.display = 'none';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('errorText').textContent = message;
    document.getElementById('addTopicForm').style.display = 'block';
}

// Reset error messages when user starts typing
document.addEventListener('input', function(e) {
    if (e.target.matches('input, textarea, select')) {
        const errorMsg = document.getElementById('errorMessage');
        if (errorMsg && errorMsg.style.display !== 'none') {
            document.getElementById('addTopicForm').style.display = 'block';
        }
    }
});
