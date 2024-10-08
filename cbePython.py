from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import mysql.connector

# Step 1: Convert text to speech (TTS) and save as MP3
def text_to_speech(text, mp3_filename="output.mp3"):
    tts = gTTS(text)
    tts.save(mp3_filename)
    print(f"Audio file saved as {mp3_filename}")

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
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Step 3: Store the recognized text into the MySQL database
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

# 1. Convert text to MP3
text = "A.P.J. Abdul Kalam (born October 15, 1931, Rameswaram, India—died July 27, 2015, Shillong) was an Indian scientist and politician who played a leading role in the development of India’s missile and nuclear weapons programs. He was president of India from 2002 to 2007."
text_to_speech(text, "passage.mp3")

# 2. Convert MP3 to text directly
audio_text = speech_to_text_from_mp3("passage.mp3")

# 3. Store the recognized text in the database
if audio_text:
    store_transcript_in_db(audio_text)
