const express = require('express');
const app = express();
const PORT = 3000;

// Middleware to parse POST data
app.use(express.urlencoded({ extended: true }));

// Set view engine to EJS
app.set('view engine', 'ejs');

// Route to render the index page
app.get('/', (req, res) => {
    res.render('index', { message: null }); // Initially pass null for the message
});

// Route to handle the form submission
app.post('/criminal/search', (req, res) => {
    const { criminalId } = req.body;

    // Example logic to handle the form submission
    if (criminalId === '123') {
        res.send('Criminal found!'); // Replace with actual logic
    } else {
        res.render('index', { message: 'Criminal not found!' }); // Pass the error message
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
