// app/static/js/main.js

// Audio handling
let audioContext = null;
let alarmSound = null;
let currentAlarmSource = null;

// Initialize audio context
function initAudio() {
    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    fetch('/static/sounds/alarm.mp3')
        .then(response => response.arrayBuffer())
        .then(arrayBuffer => audioContext.decodeAudioData(arrayBuffer))
        .then(audioBuffer => {
            alarmSound = audioBuffer;
        })
        .catch(error => console.error('Error loading alarm sound:', error));
}

// Play alarm sound
function playAlarm() {
    if (!audioContext) initAudio();
    
    if (currentAlarmSource) {
        currentAlarmSource.stop();
    }
    
    const source = audioContext.createBufferSource();
    source.buffer = alarmSound;
    source.connect(audioContext.destination);
    source.loop = true;
    source.start();
    currentAlarmSource = source;
    return source;
}

// Stop alarm sound
function stopAlarm() {
    if (currentAlarmSource) {
        currentAlarmSource.stop();
        currentAlarmSource = null;
    }
}

// Alarm management
document.getElementById('alarm-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const timeInput = document.getElementById('alarm-time');
    const time = timeInput.value;
    
    try {
        const response = await fetch('/api/alarms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ time }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            location.reload();
        } else {
            alert(data.error || 'Failed to add alarm');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add alarm');
    }
});

async function deleteAlarm(alarmId) {
    if (!confirm('Are you sure you want to delete this alarm?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/alarms/${alarmId}`, {
            method: 'DELETE',
        });
        
        if (response.ok) {
            location.reload();
        } else {
            const data = await response.json();
            alert(data.error || 'Failed to delete alarm');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete alarm');
    }
}

// Check for active alarms
async function checkAlarms() {
    try {
        const response = await fetch('/api/check-alarms');
        const data = await response.json();
        
        if (data.alarm_triggered) {
            playAlarm();
            window.location.href = `/challenge/${data.challenge_id}`;
        }
    } catch (error) {
        console.error('Error checking alarms:', error);
    }
}

// Challenge page functions
let lastActivityTime = Date.now();
const INACTIVITY_TIMEOUT = 30000; // 30 seconds

function updateActivity() {
    lastActivityTime = Date.now();
    if (!document.getElementById('challenge-page')) return;
    
    const timeInactive = Date.now() - lastActivityTime;
    if (timeInactive > INACTIVITY_TIMEOUT) {
        playAlarm();
    }
}

// Track user activity
document.addEventListener('mousemove', updateActivity);
document.addEventListener('keypress', updateActivity);
document.addEventListener('click', updateActivity);

async function submitSolution() {
    const editor = document.getElementById('code-editor');
    const resultsDiv = document.getElementById('test-results');
    const code = editor.value;
    const challengeId = window.location.pathname.split('/').pop();
    
    resultsDiv.innerHTML = 'Running tests...';
    
    try {
        const response = await fetch('/api/verify-solution', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                challenge_id: challengeId,
                solution: code,
            }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
            formatAndDisplayResults(data);
            if (data.all_passed) {
                stopAlarm();
                alert('Congratulations! All tests passed. Returning to main page...');
                setTimeout(() => {
                    window.location.href = '/';
                }, 2000);
            }
        } else {
            resultsDiv.innerHTML = `<div class="test-result-error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = '<div class="test-result-error">Error submitting solution</div>';
    }
}

function formatAndDisplayResults(results) {
    const resultsDiv = document.getElementById('test-results');
    let html = '';
    
    results.test_results.forEach((test, index) => {
        const resultClass = test.passed ? 'test-result-success' : 'test-result-failure';
        html += `
            <div class="${resultClass}">
                <div><strong>Test ${index + 1}:</strong> ${test.description}</div>
                <div>Input: ${JSON.stringify(test.input)}</div>
                <div>Expected: ${JSON.stringify(test.expected)}</div>
                <div>Got: ${JSON.stringify(test.actual)}</div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

function resetCode() {
    const editor = document.getElementById('code-editor');
    const starterCode = editor.getAttribute('data-starter-code');
    
    if (confirm('Are you sure you want to reset your code to the starter template?')) {
        editor.value = starterCode;
    }
}

// Initialize audio and start alarm checking if on main page
if (document.getElementById('alarm-form')) {
    initAudio();
    setInterval(checkAlarms, 1000);
}
