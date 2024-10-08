from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import mysql.connector

# Step 1: Convert text to speech (TTS) and save as MP3
def text_to_speech(text, mp3_filename="output.mp3"):
    tts = gTTS(text)
    tts.save(mp3_filename)
    print(f"Audio file saved as {mp3_filename}")

# Step 2: Convert MP3 to WAV using pydub
def convert_mp3_to_wav(mp3_filename, wav_filename="output.wav"):
    sound = AudioSegment.from_mp3(mp3_filename)
    sound.export(wav_filename, format="wav")
    print(f"Converted {mp3_filename} to {wav_filename}")
    return wav_filename

# Step 3: Convert speech to text (Speech-to-Text)
def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("Text from audio: ", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

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

# 1. Convert text to MP3
text = "A.P.J. Abdul Kalam (born October 15, 1931, Rameswaram, India—died July 27, 2015, Shillong) was an Indian scientist and politician who played a leading role in the development of India’s missile and nuclear weapons programs. He was president of India from 2002 to 2007."
text_to_speech(text, "passage.mp3")

# 2. Convert MP3 to WAV
wav_filename = convert_mp3_to_wav("passage.mp3")

# 3. Convert WAV back to text
audio_text = speech_to_text(wav_filename)

# 4. Store the recognized text in the database
if audio_text:
    store_transcript_in_db(audio_text)
