let currentProblemId = null;

function getProblem() {
    fetch('/get_problem', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: 1 }), // You can adjust difficulty as needed
    })
    .then(response => response.json())
    .then(data => {
        currentProblemId = data.id;
        document.getElementById('problem').textContent = data.question;
        document.getElementById('answer').value = '';
        document.getElementById('feedback').textContent = '';
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
            feedbackElement.textContent = 'Correct! ' + data.explanation;
            feedbackElement.className = 'feedback correct';
        } else {
            feedbackElement.textContent = 'Incorrect. ' + data.explanation;
            feedbackElement.className = 'feedback incorrect';
        }
        document.getElementById('score').textContent = 'Score: ' + data.score;
        
        // Get next problem after a short delay
        setTimeout(getProblem, 3000);
    });
}

// Initialize the game
document.addEventListener('DOMContentLoaded', function() {
    getProblem();
    document.getElementById('submit-btn').addEventListener('click', checkAnswer);
});
