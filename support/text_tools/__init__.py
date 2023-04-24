import nltk
from nltk.corpus import stopwords
from loguru import logger
import os

import re


try:
    if not os.path.exists('support/text_tools/stopwordsexist'):
        nltk.download('stopwords')
        os.system('touch support/text_tools/stopwordsexist')
    else:
        pass
except Exception as e:
    logger.warning(f"Failed to download stopwords | {e}")


def get_keywords(text,number):
    cleantext = re.sub('\W+',' ', text )
    words = cleantext.split()
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    # Sort the dictionary by frequency
    sorted_word_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

    # Get the top 10 most common keywords
    top_keywords = [w[0] for w in sorted_word_freq[:number]]

    return top_keywords