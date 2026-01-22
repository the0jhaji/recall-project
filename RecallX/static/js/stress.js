/**
 * Stress Test JavaScript
 * Handles the high-pressure recall testing experience
 */

let currentQuestionIndex = 0;
let questions = [];
let startTime = 0;
let testStartTime = 0;
const TEST_DURATION = 300; // 5 minutes in seconds
let timeRemaining = TEST_DURATION;
let stressLevel = 30;
const topicId = window.location.pathname.split('/').pop();

let testResults = {
    total_questions: 0,
    correct_answers: 0,
    responses: [],
    total_time: 0,
    avg_stress: 0
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadQuestions();
    startTest();
});

function loadQuestions() {
    fetch(`/api/generate-questions/${topicId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                questions = data.questions;
                testResults.total_questions = questions.length;
                displayQuestion();
            } else {
                showError('Failed to load questions');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error loading questions: ' + error.message);
        });
}

function startTest() {
    testStartTime = Date.now();
    startTimer();
    addStressEffects();
}

function startTimer() {
    const timerInterval = setInterval(() => {
        timeRemaining--;
        
        // Update display
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        document.getElementById('timerValue').textContent = 
            `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        // Increase stress level as time runs out
        stressLevel = Math.min(100, 30 + ((TEST_DURATION - timeRemaining) / TEST_DURATION) * 70);
        updateStressIndicator();
        
        // Add tick sound effect (visual only)
        if (timeRemaining % 10 === 0 && timeRemaining > 0) {
            playTickSound();
        }
        
        // Time's up
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            endTest();
        }
        
        // Flash warning at 30 seconds
        if (timeRemaining === 30) {
            flashWarning();
        }
    }, 1000);
}

function displayQuestion() {
    if (currentQuestionIndex >= questions.length || timeRemaining <= 0) {
        endTest();
        return;
    }

    const question = questions[currentQuestionIndex];
    startTime = Date.now();
    
    const questionHTML = `
        <div class="question-text">${question.question}</div>
        <input type="text" class="answer-input" id="answerInput" placeholder="Type your answer..." autofocus>
        <div class="confidence-selector">
            <p style="margin-bottom: 0.5rem;">How confident are you?</p>
            <div class="confidence-buttons">
                <button class="confidence-btn" data-confidence="25">😕 Low</button>
                <button class="confidence-btn" data-confidence="50">😐 Medium</button>
                <button class="confidence-btn" data-confidence="75">🤔 High</button>
                <button class="confidence-btn" data-confidence="100">😎 Very Sure</button>
            </div>
        </div>
        <button class="submit-answer-btn" onclick="submitAnswer('${question.id}', '${question.answer}')">SUBMIT ANSWER</button>
    `;
    
    document.getElementById('questionDisplay').innerHTML = questionHTML;
    document.getElementById('questionCounter').textContent = `Question ${currentQuestionIndex + 1} / ${questions.length}`;
    
    // Add confidence button listeners
    document.querySelectorAll('.confidence-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.confidence-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Allow Enter key to submit
    document.getElementById('answerInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitAnswer(question.id, question.answer);
        }
    });
}

function submitAnswer(questionId, correctAnswer) {
    const userAnswer = document.getElementById('answerInput').value;
    const confidence = document.querySelector('.confidence-btn.active');
    
    if (!userAnswer.trim()) {
        alert('Please enter an answer');
        return;
    }
    
    const responseTime = (Date.now() - startTime) / 1000;
    const confidenceValue = confidence ? parseInt(confidence.dataset.confidence) : 50;
    
    // Submit to backend
    fetch('/api/stress-test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            user_answer: userAnswer,
            response_time: responseTime,
            stress_level: Math.round(stressLevel),
            confidence: confidenceValue,
            correct_answer: correctAnswer
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Record result
            testResults.responses.push({
                question_id: questionId,
                is_correct: data.is_correct,
                response_time: responseTime,
                stress_level: Math.round(stressLevel),
                confidence: confidenceValue
            });
            
            if (data.is_correct) {
                testResults.correct_answers++;
                showCorrect();
            } else {
                showIncorrect(correctAnswer);
            }
            
            // Move to next question after 1 second
            setTimeout(() => {
                currentQuestionIndex++;
                displayQuestion();
            }, 1000);
        }
    })
    .catch(error => console.error('Error submitting answer:', error));
}

function showCorrect() {
    document.querySelector('.question-display').style.background = 'rgba(16, 185, 129, 0.2)';
    document.querySelector('.question-display').style.borderColor = '#10b981';
}

function showIncorrect(correctAnswer) {
    document.querySelector('.question-display').style.background = 'rgba(239, 68, 68, 0.2)';
    document.querySelector('.question-display').style.borderColor = '#ef4444';
}

function updateStressIndicator() {
    const stressBar = document.getElementById('stressBar');
    stressBar.style.width = stressLevel + '%';
    
    let stressLabel = 'LOW';
    let stressColor = '#10b981';
    
    if (stressLevel > 70) {
        stressLabel = 'CRITICAL';
        stressColor = '#ef4444';
    } else if (stressLevel > 50) {
        stressLabel = 'HIGH';
        stressColor = '#f59e0b';
    } else if (stressLevel > 30) {
        stressLabel = 'MEDIUM';
        stressColor = '#f59e0b';
    }
    
    stressBar.style.background = stressColor;
    document.getElementById('stressLabel').textContent = `Stress Level: ${stressLabel} (${Math.round(stressLevel)}%)`;
}

function addStressEffects() {
    // Add visual stress effects
    document.addEventListener('mousemove', function(e) {
        if (stressLevel > 70) {
            const offset = (Math.random() - 0.5) * 5;
            document.documentElement.style.transform = `translateX(${offset}px)`;
        }
    });
}

function playTickSound() {
    // Visual feedback for tick (no actual sound for demo)
    const timer = document.querySelector('.timer-display');
    timer.style.textShadow = '0 0 30px rgba(96, 165, 250, 0.8)';
    setTimeout(() => {
        timer.style.textShadow = '0 0 20px rgba(96, 165, 250, 0.5)';
    }, 100);
}

function flashWarning() {
    const container = document.querySelector('.stress-test-container');
    container.style.boxShadow = 'inset 0 0 40px rgba(239, 68, 68, 0.5)';
    setTimeout(() => {
        container.style.boxShadow = 'none';
    }, 500);
}

function endTest() {
    const totalTime = (Date.now() - testStartTime) / 1000;
    testResults.total_time = totalTime;
    testResults.avg_stress = Math.round(testResults.responses.reduce((a, r) => a + r.stress_level, 0) / testResults.responses.length);
    
    displayResults();
}

function displayResults() {
    const accuracy = (testResults.correct_answers / testResults.total_questions) * 100;
    const avgResponseTime = testResults.responses.reduce((a, r) => a + r.response_time, 0) / testResults.responses.length;
    const avgConfidence = testResults.responses.reduce((a, r) => a + r.confidence, 0) / testResults.responses.length;
    
    document.getElementById('questionDisplay').style.display = 'none';
    document.getElementById('questionCounter').style.display = 'none';
    document.getElementById('resultsPanel').style.display = 'flex';
    
    document.getElementById('accuracyValue').textContent = accuracy.toFixed(1) + '%';
    document.getElementById('timeValue').textContent = avgResponseTime.toFixed(1) + 's';
    document.getElementById('confidenceValue').textContent = avgConfidence.toFixed(0) + '%';
}

function exitTest() {
    if (confirm('Are you sure you want to exit? Your progress will be lost.')) {
        window.location.href = '/dashboard';
    }
}

function showError(message) {
    document.getElementById('questionDisplay').innerHTML = `<div style="color: white; font-size: 1.25rem;">${message}</div>`;
}
