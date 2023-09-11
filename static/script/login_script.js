document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting normally

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Send the captured data to the Flask backend
    sendDataToFlask(username, password);
});

function sendDataToFlask(username, password) {
    // Create an object to hold the data
    const data = {
        username: username,
        password: password
    };

    // Send the data to the Flask backend using AJAX (Fetch API)
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from Flask here
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
