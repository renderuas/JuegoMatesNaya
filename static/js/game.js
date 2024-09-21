let currentProblemId = null;
let currentGameId = null;
let currentSessionId = null;
let currentUserId = null;
let timerInterval = null;

function getProblem() {
    fetch('/get_problem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: 1 }),
    })
    .then(response => response.json())
    .then(data => {
        currentProblemId = data.id;
        document.getElementById('problem').textContent = data.question;
        document.getElementById('answer').value = '';
        document.getElementById('feedback').textContent = '';
        document.getElementById('next-btn').style.display = 'none';
    });
}

function checkAnswer() {
    const userAnswer = document.getElementById('answer').value;
    
    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            problem_id: currentProblemId,
            answer: userAnswer
        }),
    })
    .then(response => response.json())
    .then(data => {
        const feedbackElement = document.getElementById('feedback');
        if (data.correct) {
            feedbackElement.textContent = '¡Muy bien! ' + data.explanation;
            feedbackElement.className = 'feedback correct';
        } else {
            feedbackElement.textContent = '¡Ups! ' + data.explanation + ' ¡Inténtalo de nuevo!';
            feedbackElement.className = 'feedback incorrect';
        }
        document.getElementById('score').textContent = 'Tu puntuación: ' + data.score;
        
        // Show the "Next" button
        document.getElementById('next-btn').style.display = 'inline-block';
    });
}

function nextProblem() {
    getProblem();
}

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    getProblem();
    document.getElementById('submit-btn').addEventListener('click', checkAnswer);
    document.getElementById('next-btn').addEventListener('click', nextProblem);
});

// Multiplayer game functions
function initMultiplayerGame(sessionId, userId) {
    currentSessionId = sessionId;
    currentUserId = userId;
    getMultiplayerProblem();
    startTimer();
    
    document.getElementById('submit-btn').addEventListener('click', checkMultiplayerAnswer);
}

function getMultiplayerProblem() {
    fetch('/multiplayer/get_problem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ session_id: currentSessionId }),
    })
    .then(response => response.json())
    .then(data => {
        currentGameId = data.game_id;
        document.getElementById('problem').textContent = data.question;
        document.getElementById('answer').value = '';
        resetTimer();
    });
}

function checkMultiplayerAnswer() {
    const userAnswer = document.getElementById('answer').value;
    
    fetch('/multiplayer/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: currentGameId,
            answer: userAnswer
        }),
    })
    .then(response => response.json())
    .then(data => {
        updateScores(data.player1_score, data.player2_score);
        getMultiplayerProblem();
    });
}

function updateScores(player1Score, player2Score) {
    document.getElementById('player1-score').textContent = player1Score;
    document.getElementById('player2-score').textContent = player2Score;
}

function startTimer() {
    let timeLeft = 30;
    const timerElement = document.getElementById('time-left');
    
    timerInterval = setInterval(() => {
        timeLeft--;
        timerElement.textContent = timeLeft;
        
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            checkMultiplayerAnswer();
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timerInterval);
    startTimer();
}

// Long-polling function to keep game state synchronized
function pollGameState() {
    fetch(`/multiplayer/game_state/${currentSessionId}`)
    .then(response => response.json())
    .then(data => {
        updateScores(data.player1_score, data.player2_score);
        if (data.game_ended) {
            endGame(data.winner);
        } else {
            setTimeout(pollGameState, 1000);
        }
    });
}

function endGame(winner) {
    clearInterval(timerInterval);
    const gameResultElement = document.getElementById('game-result');
    gameResultElement.textContent = `Game Over! ${winner} wins!`;
    gameResultElement.style.display = 'block';
}
