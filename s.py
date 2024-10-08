import mysql.connector
from gtts import gTTS
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def summarize_text(text):
    try:
        # Load model and tokenizer
        model_name = "gpt2"  # You can choose a more powerful model if needed
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        # Create a prompt for summarization
        prompt = f"Summarize the following text:\n{text}\nSummary:"
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

        # Generate summary
        outputs = model.generate(inputs["input_ids"], max_length=100, num_return_sequences=1, do_sample=False)
        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract the summary part from the generated text
        summary = summary.split("Summary:")[-1].strip()
        print("Summary:", summary)
        return summary
    except Exception as e:
        print("Error in summarization:", e)
        return None

def convert_text_to_speech(summary):
    try:
        tts = gTTS(text=summary, lang='en')
        tts.save("convertedtext.mp3")
        print("Text converted successfully")
    except Exception as e:
        print("Error in text-to-speech conversion:", e)

def store_summary_in_db(summary):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='text_summary'
        )
        cursor = conn.cursor()
        insert_query = "INSERT INTO summaries (summary_text) VALUES (%s)"
        cursor.execute(insert_query, (summary,))
        conn.commit()
        print("Text stored in the database successfully")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

text = ("A looking for food. Unknowingly, she got caught in a trap. "
            "She tried hard to get out of it, and it was only after a tough struggle that she could get free. "
            "Feeling greatly relieved, she walked away. But something seemed amiss. When she turned back, "
            "she noticed to her shock that her beautiful tail had been cut off. "
            "It had been left behind in the trap.")

summary = summarize_text(text)
if summary:
    convert_text_to_speech(summary)
    store_summary_in_db(summary)