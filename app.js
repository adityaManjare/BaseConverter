// Function to handle the form submission for binary operations
document.getElementById('operation-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const binary1 = document.getElementById('binary1').value;
    const binary2 = document.getElementById('binary2').value;
    const num_bits = parseInt(document.getElementById('num_bits').value, 10);
    const operation = document.getElementById('operation').value;
    const representation = document.getElementById('representation').value;
    const resultTextElement = document.getElementById('operation-result-text');

    const payload = {
        binary1: binary1,
        binary2: binary2,
        num_bits: num_bits,
        operation: operation,
        representation: representation
    };

    try {
        const response = await fetch('/binary/operation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            let errorMessage = 'An unknown error occurred';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.error || errorMessage;
            } catch {
                errorMessage = `Server responded with status ${response.status} but no valid error message.`;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();

        if (data.error) {
            resultTextElement.textContent = `Error: ${data.error}`;
            return;
        }

        let formattedOutput = '';
        if (data.operation.includes('division')) {
            formattedOutput = `Operation: ${data.operation}\n` +
                              `Representation: ${data.representation}\n` +
                              `Quotient: ${data.quotient}\n` +
                              `Remainder: ${data.remainder}`;
        } else if (data.operation.includes('multiplication')) {
            formattedOutput = `Operation: ${data.operation}\n` +
                              `Representation: ${data.representation}\n` +
                              `Result: ${data.result}\n` +
                              `Result Bits: ${data.result_bits}`;
        } else {
            formattedOutput = `Operation: ${data.operation}\n` +
                              `Representation: ${data.representation}\n` +
                              `Result: ${data.result}`;
        }
        
        resultTextElement.textContent = formattedOutput;

    } catch (error) {
        resultTextElement.textContent = `An error occurred: ${error.message}`;
    }
});

// Function to handle the form submission for base conversion
document.getElementById('conversion-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const number = document.getElementById('number').value;
    const from_base = parseInt(document.getElementById('from_base').value, 10);
    const to_base = parseInt(document.getElementById('to_base').value, 10);
    const resultTextElement = document.getElementById('conversion-result-text');

    const payload = {
        number: number,
        from_base: from_base,
        to_base: to_base
    };

    try {
        const response = await fetch('/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            let errorMessage = 'An unknown error occurred';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.error || errorMessage;
            } catch {
                errorMessage = `Server responded with status ${response.status} but no valid error message.`;
            }
            throw new Error(errorMessage);
        }

        const data = await response.json();

        // Fix: Display the raw JSON from the server to debug the backend.
        // This will show you exactly what your baseConverter function is returning.
        resultTextElement.textContent = JSON.stringify(data, null, 2);

    } catch (error) {
        resultTextElement.textContent = `An error occurred: ${error.message}`;
    }
});
