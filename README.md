# GPT-CTF
This Flask application is designed to detect Capture The Flag (CTF) flags from input data using GPT-4. The app queries the GPT-4 model with provided information, checks if the response contains a CTF flag, and sends an alert if a flag is detected. This project leverages OpenAI's GPT-4 model to assist in CTF competitions by detecting flags from provided input data. The app is designed to streamline the process of flag detection by automating the query and response analysis using advanced AI models.

## Features
- Accepts input data and queries GPT-4.
- Detects CTF flags within the GPT-4 response.
- Sends alerts when a CTF flag is detected.

## Requirements

Ensure you have the following installed:

- Python 3.7+
- Flask
- OpenAI Python Client
- OpenAI tokens

All required Python packages are listed in the `requirements.txt` file.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ctf-flag-detector.git
    cd ctf-flag-detector
    ```

2. **Set up a virtual environment (optional but recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the environment variable:**

    The application requires an OpenAI API key to function. Set it as an environment variable:

    ```bash
    export OPENAI_API_KEY='your-openai-api-key-here'
    ```

    Alternatively, you can create a `.env` file in the root of the project and add your API key there:

    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ```

## Usage

1. **Run the Flask app:**

    ```bash
    flask run
    ```

2. **Send a POST request with the necessary information:**

    The Flask app will listen for incoming data and query GPT-4 to check for CTF flags. If a flag is detected, an alert will be sent.

    Example cURL request:

    ```bash
    curl -X POST http://127.0.0.1:5000/detect -d "input_data=your_input_here"
    ```

3. **Monitor the output:**

    The app will return a response indicating whether a CTF flag was detected.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
