let currentProblemId = null;

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
        console.log('Problem data:', data);  // Keep this for debugging
        currentProblemId = data.id;
        document.getElementById('question').textContent = data.question;
        document.getElementById('answer').value = '';
        document.getElementById('feedback').textContent = '';
        document.getElementById('submit-btn').style.display = 'inline-block';
        document.getElementById('next-btn').style.display = 'none';
    })
    .catch(error => {
        console.error('Error fetching problem:', error);
        document.getElementById('question').textContent = 'Error loading problem';
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
            feedbackElement.textContent = translations.awesome + ' 🎉 ' + data.explanation;
            feedbackElement.className = 'feedback correct celebrate';
        } else {
            feedbackElement.textContent = translations.oops + ' 😕 ' + data.explanation + ' ' + translations.tryAgain;
            feedbackElement.className = 'feedback incorrect';
        }
        document.getElementById('score-value').textContent = data.score;
        
        document.getElementById('submit-btn').style.display = 'none';
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
