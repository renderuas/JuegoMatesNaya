function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function updateLeaderboard() {
    fetch('/api/leaderboard')
        .then(response => response.json())
        .then(data => {
            const leaderboardElement = document.getElementById('leaderboard');
            leaderboardElement.innerHTML = '<h3>Leaderboard</h3>';
            const list = document.createElement('ol');
            data.forEach(user => {
                const item = document.createElement('li');
                item.textContent = `${user.username}: ${user.score}`;
                list.appendChild(item);
            });
            leaderboardElement.appendChild(list);
        });
}

function updateUserProgress() {
    fetch('/api/user_progress')
        .then(response => response.json())
        .then(data => {
            const progressElement = document.getElementById('user-progress');
            progressElement.innerHTML = '<h3>Your Recent Progress</h3>';
            const list = document.createElement('ul');
            data.forEach(progress => {
                const item = document.createElement('li');
                item.textContent = `Problem ${progress.problem_id}: ${progress.is_correct ? 'Correct' : 'Incorrect'} (${formatDate(progress.timestamp)})`;
                list.appendChild(item);
            });
            progressElement.appendChild(list);
        });
}
