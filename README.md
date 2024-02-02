# Behavioral Interview Agent API

## Overview

The Behavioral Interview Agent API is designed to facilitate interactive, AI-driven interviews by processing audio inputs from users, analyzing the content, and generating responsive audio outputs. It integrates Google Cloud's Speech-to-Text and Text-to-Speech services along with OpenAI's GPT-3.5-turbo to provide a seamless conversational experience.

## Features

- **Audio Input Processing**: Accepts user's audio inputs and converts them into text for further processing.
- **AI-Driven Interaction**: Leverages the GPT-3.5-turbo model from OpenAI to understand the context and content of the user's query and generate an appropriate textual response.
- **Audio Output Generation**: Converts the AI-generated textual responses back into audio, facilitating a natural dialogue flow.

## API Endpoints

The API comprises two primary endpoints:

### 1. Version Endpoint

- **Endpoint**: `GET /version`
- **Description**: Provides the current version of the API.
- **Response**: A plain text containing the version number, e.g., `0.0.1`.

### 2. Respond Endpoint

- **Endpoint**: `POST /respond`
- **Description**: Processes an uploaded audio file from the user, generating a corresponding audio response.
- **Request**: A `multipart/form-data` request with an audio file.
- **Response**: An audio stream in MP3 format containing the AI-generated response.

## Getting Started

To utilize this API, follow the steps outlined below:

### Prerequisites

- Python 3.6+
- FastAPI
- Uvicorn
- Google Cloud Speech-to-Text API
- Google Cloud Text-to-Speech API
- OpenAI API (GPT-3.5-turbo)

### Installation

1. Clone the API repository to your local environment.
2. Navigate to the project directory and set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
```
pip install fastapi uvicorn python-multipart google-cloud-speech google-cloud-texttospeech openai
```

### Configuration

Google Cloud Services: Set up a Google Cloud project, enable Speech-to-Text and Text-to-Speech APIs, and download your service account key. Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
OpenAI: Obtain an API key from OpenAI and replace "your_openai_api_key" in the application code with your actual API key.
Running the API

Start the API server using Uvicorn with the following command:
```
uvicorn main:API --reload
```
This will host the API locally, making it accessible via http://localhost:8000.