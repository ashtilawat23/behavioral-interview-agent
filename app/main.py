from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from google.cloud import speech, texttospeech
from openai import OpenAI

# Initialize FastAPI application with basic details
API = FastAPI(title='Behavioral Interview Agent', version="0.0.1", docs_url='/')

# Read API description from README.md
with open("README.md", "r") as file:
    next(file)  # Skip the first line
    description = file.read()
API.description = description

# Configure CORS middleware for cross-origin requests
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Initialize clients for Google Cloud and OpenAI services
speech_client = speech.SpeechClient()
tts_client = texttospeech.TextToSpeechClient()
openai_client = OpenAI(api_key="your_openai_api_key")

# Define endpoint to return the current API version
@API.get("/version", tags=["General"])
async def version():
    """
    Returns the current version of the API.
    """
    return API.version

# Define endpoint to process audio input and generate audio response
@API.post("/respond", tags=["Interaction"])
async def respond(audio: UploadFile = File(...)):
    """
    Processes audio input by converting it to text, generating a response using GPT-3.5-turbo,
    and converting the text response back to audio to be sent to the client.
    """

    # Convert uploaded audio file to text using Google Speech-to-Text API
    audio_content = await audio.read()
    audio_input = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US"
    )
    stt_response = speech_client.recognize(config=config, audio=audio_input)
    transcript = stt_response.results[0].alternatives[0].transcript

    # Generate a text response using OpenAI's GPT-3.5-turbo
    gpt_response = openai_client.create_completion(
        model="gpt-3.5-turbo",
        prompt=transcript,
        max_tokens=150
    )
    response_text = gpt_response.choices[0].text.strip()

    # Convert the text response back to audio using Google Text-to-Speech API
    synthesis_input = texttospeech.SynthesisInput(text=response_text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    tts_response = tts_client.synthesize_speech(
        input=synthesis_input,
        voice=voice_params,
        audio_config=audio_config
    )

    # Return the generated audio response to the client
    return Response(content=tts_response.audio_content, media_type="audio/mp3")
