/**
 * Chart.js for Forgetting Curve Visualization
 * Implements Ebbinghaus Forgetting Curve with Chart.js
 */

const topicId = window.location.pathname.split('/').pop();
let chart = null;

document.addEventListener('DOMContentLoaded', function() {
    loadForgettingCurveData();
    
    // Set up stress test button
    const stressTestBtn = document.getElementById('stressTestBtn');
    if (stressTestBtn) {
        stressTestBtn.href = `/stress-test/${topicId}`;
    }
});

function loadForgettingCurveData() {
    fetch(`/api/forgetting-curve/${topicId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayChart(data);
                displayOptimalDates(data.optimal_dates);
                displayInsights(data);
            } else {
                showError(data.error || 'Failed to load forgetting curve');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Error loading forgetting curve: ' + error.message);
        });
}

function displayChart(data) {
    document.getElementById('loadingChart').style.display = 'none';
    
    const ctx = document.getElementById('forgettingCurveChart').getContext('2d');
    
    // Prepare data
    const labels = data.curve_data.map(d => 'Day ' + d.day);
    const retentionData = data.curve_data.map(d => d.retention);
    
    // Create gradient colors based on retention levels
    const backgroundColors = [];
    const borderColors = [];
    
    data.curve_data.forEach(d => {
        if (d.retention >= 70) {
            backgroundColors.push('rgba(16, 185, 129, 0.1)');
            borderColors.push('#10b981');
        } else if (d.retention >= 40) {
            backgroundColors.push('rgba(245, 158, 11, 0.1)');
            borderColors.push('#f59e0b');
        } else {
            backgroundColors.push('rgba(239, 68, 68, 0.1)');
            borderColors.push('#ef4444');
        }
    });
    
    // Destroy existing chart if any
    if (chart) {
        chart.destroy();
    }
    
    // Create new chart
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Memory Retention (%)',
                    data: retentionData,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.05)',
                    borderWidth: 3,
                    tension: 0.4,
                    pointRadius: 4,
                    pointBackgroundColor: '#6366f1',
                    pointBorderColor: 'white',
                    pointBorderWidth: 2,
                    fill: true,
                    pointHoverRadius: 6,
                    yAxisID: 'y',
                },
                {
                    label: 'Forget Probability (%)',
                    data: data.curve_data.map(d => d.forget_probability),
                    borderColor: '#ef4444',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    fill: false,
                    yAxisID: 'y1',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        font: { size: 12 },
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: { size: 14 },
                    bodyFont: { size: 12 },
                    cornerRadius: 4,
                    displayColors: true,
                    callbacks: {
                        title: function(context) {
                            return 'Day ' + context[0].label.split(' ')[1];
                        },
                        label: function(context) {
                            return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '%';
                        }
                    }
                }
            },
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    title: {
                        display: true,
                        text: 'Retention %',
                        font: { size: 12 }
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    title: {
                        display: true,
                        text: 'Forget Probability %',
                        font: { size: 12 }
                    },
                    min: 0,
                    max: 100,
                    grid: {
                        drawOnChartArea: false
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(200, 200, 200, 0.1)'
                    }
                }
            }
        }
    });
}

function displayOptimalDates(optimalDates) {
    const container = document.getElementById('optimalDatesContainer');
    
    const html = optimalDates.map(date => `
        <div class="date-item">
            <strong>Day ${date.day}</strong>
            <div>${date.date}</div>
            <div style="color: #6366f1; font-weight: bold;">${date.retention.toFixed(0)}% Retention</div>
        </div>
    `).join('');
    
    container.innerHTML = html;
}

function displayInsights(data) {
    document.getElementById('topicName').textContent = data.topic_name;
    document.getElementById('strengthValue').textContent = data.topic_strength.toFixed(2);
    
    // Calculate next action
    let nextAction = 'Start stress testing to improve retention';
    if (data.topic_strength > 3) {
        nextAction = 'Your strength is good. Keep practicing consistently.';
    } else if (data.topic_strength > 2) {
        nextAction = 'Moderate strength. Plan revisions for day 3.';
    } else {
        nextAction = 'Weak retention. Revise immediately and then daily.';
    }
    
    document.getElementById('nextAction').textContent = nextAction;
}

function showError(message) {
    document.getElementById('loadingChart').innerHTML = `<div style="color: red;">${message}</div>`;
}
