const API_URL = '/identify';

const form = document.getElementById('identifyForm');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phoneNumber');
const warningMessage = document.getElementById('warningMessage');
const submitBtn = document.getElementById('submitBtn');
const btnText = document.getElementById('btnText');
const btnSpinner = document.getElementById('btnSpinner');
const resultContainer = document.getElementById('resultContainer');
const jsonOutput = document.getElementById('jsonOutput');

function syntaxHighlight(json) {
    if (typeof json != 'string') {
        json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Reset states
    warningMessage.classList.add('hidden');
    resultContainer.classList.add('hidden');

    // Get values. Convert empty strings to null as expected by the backend logic.
    const email = emailInput.value.trim() || null;
    const phoneNumber = phoneInput.value.trim() || null;

    // Validation: Both cannot be null at the same time
    if (!email && !phoneNumber) {
        warningMessage.classList.remove('hidden');
        return;
    }

    // Set Loading State
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-75', 'cursor-not-allowed');
    btnText.textContent = 'Processing...';
    btnSpinner.classList.remove('hidden');

    const payload = {
        email: email,
        phoneNumber: phoneNumber
    };

    try {
        // Make the POST request to the dynamic /identify endpoint
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        // Format and display the beautiful JSON
        jsonOutput.innerHTML = syntaxHighlight(data);
        resultContainer.classList.remove('hidden');

    } catch (error) {
        console.error("Error during identification:", error);

        // Fallback display for network errors so you can see it failed gracefully
        const errorJson = {
            error: "Failed to connect to the backend.",
            message: error.message,
            tip: "Make sure your backend server is running and can handle requests at " + API_URL
        };
        jsonOutput.innerHTML = syntaxHighlight(errorJson);
        resultContainer.classList.remove('hidden');
    } finally {
        // Reset Loading State
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75', 'cursor-not-allowed');
        btnText.textContent = 'Identify Contact';
        btnSpinner.classList.add('hidden');
    }
});