import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist

# Custom Summarize Function using a prompt to extract key points from all sentences
def custom_summarize(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    
    # Tokenize words and remove stopwords
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    
    # Get word frequency distribution
    freq_dist = FreqDist(words)
    
    # Sort words by frequency
    important_words = [word for word, freq in freq_dist.most_common(10)]
    print("Important words:", important_words)
    
    # Extract sentences that contain important words
    extracted_sentences = []
    for sentence in sentences:
        if any(word in sentence.lower() for word in important_words):
            extracted_sentences.append(sentence)
    
    # Combine all relevant sentences into a summary
    summarized_text = " ".join(extracted_sentences)
    
    return summarized_text

# Sample text
text = "A.P.J. Abdul Kalam (born October 15, 1931, Rameswaram, India—died July 27, 2015, Shillong) was an Indian scientist and politician who played a leading role in the development of India’s missile and nuclear weapons programs. He was president of India from 2002 to 2007. Kalam is remembered as the 'Missile Man of India' for his pivotal role in the development of India’s ballistic missiles. He also held numerous academic positions in India."

# Call the custom summarize function
summary = custom_summarize(text)
print("Summarized Text:", summary)
