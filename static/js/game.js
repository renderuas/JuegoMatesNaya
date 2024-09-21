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
        console.log('Problem data:', data);  // Add this line for debugging
        currentProblemId = data.id;
        document.getElementById('text-question').textContent = data.text_question;
        document.getElementById('numerical-question').textContent = data.numerical_question;
        document.getElementById('answer').value = '';
        document.getElementById('feedback').textContent = '';
        document.getElementById('next-btn').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));  // Add this line to catch any errors
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
            feedbackElement.textContent = '{{ _("Awesome!") }} 🎉 ' + data.explanation;
            feedbackElement.className = 'feedback correct celebrate';
        } else {
            feedbackElement.textContent = '{{ _("Oops!") }} 😕 ' + data.explanation + ' {{ _("Let\'s try again!") }}';
            feedbackElement.className = 'feedback incorrect';
        }
        document.getElementById('score-value').textContent = data.score;
        
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
