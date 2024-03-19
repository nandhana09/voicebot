import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import json
import random

# Load the dataset 
with open(r'E:\voicebot\dataset\intents.json') as file:
    data = json.load(file)
 
# Initialize the speech recognizer
recognizer = sr.Recognizer()

def get_response(tag):
    """Get a random response from the dataset for a given tag."""
    for intent in data['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])

def speech_to_text():
    """Convert speech to text."""
    with sr.Microphone() as source:
        st.write("Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            st.write("You said:", text)
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            st.write("Could not request results from Google Speech Recognition service; {0}".format(e))
            return ""

def text_to_speech(text):
    """Convert text to speech and play it."""
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")  # On Windows

if __name__ == "__main__":
    st.title("VoiceBot")
    while True:
        # Convert speech to text
        input_text = speech_to_text().strip()

        # Process the input text
        if input_text:
            for intent in data['intents']:
                for pattern in intent['patterns']:
                    if pattern.lower() in input_text.lower():
                        response = get_response(intent['tag'])
                        st.write("Bot:", response)
                        text_to_speech(response)
                        break
                else:
                    continue
                break
