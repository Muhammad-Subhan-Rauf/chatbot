import speech_recognition as sr

from gtts import gTTS
import pygame
from io import BytesIO

def text_to_speech(text="Say something you cheeky twat", language='en'):
    # Create a gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Save the speech as a BytesIO object
    speech_data = BytesIO()
    tts.write_to_fp(speech_data)
    speech_data.seek(0)

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the speech data
    pygame.mixer.music.load(speech_data)

    # Play the speech
    pygame.mixer.music.play()

    # Wait for the speech to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Example usage:




def speech_to_text():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said: {}".format(text))
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        text_to_speech("Sorry, could not understand audio.")
        return False
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))
        text_to_speech("Could not request results from Google Web Speech API; {0}".format(e))
        return False


