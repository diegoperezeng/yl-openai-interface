# yl-openai-interface
# GPT Chat App

This is a simple chat application that uses OpenAI's GPTs models to generate responses to user input. The application is built using Python's Tkinter library for the graphical user interface, and OpenAI's API for the chat functionality.

## Installation

Before running the application, you need to install the necessary Python libraries. You can do this by running the following command:

```bash
pip install tkinter screeninfo openai
```

## Configuration

The application requires two JSON files for configuration: `config.json` and `engines.json`.

### Config.json

This file contains the OpenAI API key and the engine ID. The structure of the file should be as follows:

```json
{
    "openai_api_key": "<Your OpenAI API Key>",
    "engine": "text-davinci-002"
}
```

Replace `<Your OpenAI API Key>` with your actual OpenAI API key. The `engine` value is optional and defaults to `text-davinci-002` if not provided.

### Engines.json

This file contains a list of engine IDs that the application will use to generate responses. The structure of the file should be as follows:

```json
[
    "text-davinci-002",
    "text-curie-002",
    ...
]
```

If the `engines.json` file is not found, the application will fetch the list of available engines from OpenAI and save it to this file.

## Usage

To start the application, simply run the Python script:

```bash
python gpt_chat_app.py
```

In the application, you can select an engine from the dropdown menu, enter your request in the "Request" field, and click the "Submit" button. The response from the selected engine will appear in the "Response" field. The chat history is displayed on the left and saved to a file called `chat_history.json`.

## Troubleshooting

If you encounter any errors, make sure your OpenAI API key is correct and that you have internet access. If the problem persists, please open an issue on the project's GitHub page.
