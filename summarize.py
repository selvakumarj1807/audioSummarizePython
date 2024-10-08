import re
import nltk
import spacy  # For Named Entity Recognition (NER)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import mysql.connector

# Load Spacy's NER model
nlp = spacy.load("en_core_web_sm")

# Step 1: Convert text to speech (TTS) and save as MP3
def text_to_speech(text, mp3_filename="output.mp3"):
    tts = gTTS(text)
    tts.save(mp3_filename)
    print(f"Audio file saved as {mp3_filename}")
    print('----------------------------------------------------------------')
    print('')

# Step 2: Convert MP3 to text (Speech-to-Text)
def speech_to_text_from_mp3(mp3_filename):
    recognizer = sr.Recognizer()

    # Load the MP3 file using AudioSegment from pydub
    audio = AudioSegment.from_mp3(mp3_filename)
    
    # Export the MP3 to raw audio data in a format recognizable by SpeechRecognition
    wav_data = audio.export(format="wav")

    # Use speech recognition with the raw WAV data
    with sr.AudioFile(wav_data) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        print("Text from MP3 audio: ", text)
        print('----------------------------------------------------------------')
        print('')
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Step 3: Extract Key Entities (Date, Number, Name, Locations) from the text
def extract_entities(text):
    # Use Spacy's Named Entity Recognition (NER) to identify names, locations, and dates
    doc = nlp(text)
    
    names = []
    dates = []
    locations = []
    
    # Loop through identified entities
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            names.append(ent.text)
        elif ent.label_ == "DATE":
            dates.append(ent.text)
        elif ent.label_ in ["GPE", "LOC"]:
            locations.append(ent.text)

    # Extract numbers or years (4-digit numbers) using regex
    numbers = re.findall(r'\b\d{1,4}\b', text)

    print("Extracted Information:")
    print("----------------------")
    print("Names:", names)
    print("Dates:", dates)
    print("Locations:", locations)
    print("Numbers:", numbers)
    print('----------------------------------------------------------------')
    print('')

    return {
        "names": names,
        "dates": dates,
        "locations": locations,
        "numbers": numbers
    }

# Custom Summarize Function using extracted entities
def custom_summarize(text):
    entities = extract_entities(text)
    
    summarized_text = f"Names: {', '.join(entities['names'])}, Dates: {', '.join(entities['dates'])}, Locations: {', '.join(entities['locations'])}, Numbers: {', '.join(entities['numbers'])}"
    
    print('Summarize the passage : ')
    print('------------------------')
    print(summarized_text) 
    print('----------------------------------------------------------------')
    print('')
    
    return summarized_text

# Step 4: Store the recognized text into the MySQL database
def store_transcript_in_db(transcript):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="text_summary"  # Replace with your database name
        )
        
        cursor = connection.cursor()
        insert_query = "INSERT INTO summaries (summary_text) VALUES (%s)"
        cursor.execute(insert_query, (transcript,))
        connection.commit()

        print("Transcript stored in the database.")
    
    except mysql.connector.Error as error:
        print(f"Failed to store transcript in database: {error}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Full Project Flow
text = "A.P.J. Abdul Kalam (born October 15, 1931, Rameswaram, India—died July 27, 2015, Shillong) was an Indian scientist and politician who played a leading role in the development of India’s missile and nuclear weapons programs. He was president of India from 2002 to 2007."

# 1. Convert text to MP3
text_to_speech(text, "passage.mp3")

# 2. Convert MP3 to text directly
audio_text = speech_to_text_from_mp3("passage.mp3")

# 3. Custom Summarize Function using a prompt to extract key points from all sentences
if audio_text:
    summary = custom_summarize(audio_text)

# 4. Store the recognized text in the database
if summary:
    store_transcript_in_db(summary)
