// Retrieve DOM elements
const btnSubmit = document.getElementById('btnSubmit');
const btnClose = document.querySelector('.closeButton');
const newsContentElement = document.getElementById('newsContent');
const containtValidate = document.getElementById('containtValidate');
const containResult = document.getElementById('containResult');
const checkBoxMode = document.getElementById('flexSwitchCheckChecked');

// Function to display prediction result after fetching from the server
const displayResult = (prediction, probability) => {
    let trueIcon = document.getElementById('trueIcon');
    let fakeIcon = document.getElementById('fakeIcon');
    let resultText = document.getElementById('resultText');
    let descrpitionForPercent = document.getElementById('descrpitionForPercent');

    var progressBar = document.querySelector('.progress-bar');
    var progressBarBefore = window.getComputedStyle(progressBar, '::before');

    let percentResult = Math.round(probability * 100);

    if (prediction == 'fake') {
        trueIcon.style.display = 'none';
        fakeIcon.style.display = 'inline-block';
        resultText.innerText = 'Fake news';
        descrpitionForPercent.innerText = `The news is ${percentResult}% fake!`;
        progressBar.style.setProperty('--progress-content', '"' + percentResult + '%"');
        // progressBar.style.background = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(rgb(65, 138, 235) ${percentResult}, rgb(136, 205, 236) 0)`;
        progressBar.style.background = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(rgb(227, 24, 24) ${percentResult}%, rgb(214, 140, 140) 0)`;
    } else {
        trueIcon.style.display = 'inline-block';
        fakeIcon.style.display = 'none';
        resultText.innerText = 'True news';
        descrpitionForPercent.innerText = `The news is ${percentResult}% true!`;
        progressBar.style.setProperty('--progress-content', '"' + percentResult + '%"');
        progressBar.style.background = `radial-gradient(closest-side, white 79%, transparent 80% 100%), conic-gradient(rgb(37 203 19) ${percentResult}%, rgb(160 231 177) 0)`;
    }
}

// Event listener for submitting news information to the server
btnSubmit.addEventListener('click', function(event) {
    event.preventDefault();

    if (newsContentElement.value == '') {
        containtValidate.style.display = 'block';
        return;
    } else {
        containtValidate.style.display = 'none';
    }

    containResult.style.display = 'block';
    containResult.style.animation = 'fadeIn ease-in .5s';

    fetch('http://127.0.0.1:5000/api/predict_news', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ news_text: newsContentElement.value })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            displayResult(data.prediction, data.probability);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Event listener for hiding validation message when input changes
newsContentElement.addEventListener('input', function() {
    containtValidate.style.display = 'none';
});

// Event listener for closing the result container
btnClose.addEventListener('click', function() {
    document.getElementById('containResult').style.display = 'none';
    newsContentElement.value = '';
});

// Function to handle checkbox state change
const handleChangeCheckbox = () => {
    let labelMode = document.querySelector('.form-check-label');
    if (checkBoxMode.checked) {
        labelMode.innerText = 'Light mode';
        document.querySelector('body').style.backgroundColor = '#fff';
    } else {
        labelMode.innerText = 'Dark mode';
        document.querySelector('body').style.backgroundColor = '#170f23';
    }
};

// Add onchange event to call handleChangeCheckbox function when checkbox state changes
checkBoxMode.addEventListener('change', handleChangeCheckbox);

// Call the function once to update the initial state of the checkbox
handleChangeCheckbox();
