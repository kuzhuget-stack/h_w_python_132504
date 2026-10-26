# библиотеки
import pandas as pd
import re
import nltk
# считаем скачанный файл
df_f = pd.read_csv("reviews_new.csv")

df_f = df_f.dropna(subset=["text"])
# нижний регистр
df_f['text_lower']  = df_f['text'].str.lower()
df_f['text_lower'].head()

#Удаление URL
# Function for url's
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)
# Examples
text = "This is my website, https://www.link.com"

#Passing the function to 'text_rare'
df_f['text_lower'] = df_f['text_lower'].apply(remove_urls)


#Удаление цифр
df_f['text_lower'] = df_f['text_lower'].str.replace(r'\d+', '', regex=True)

# Удаление лишних пробелов, которые появились на месте цифр
df_f['text_lower'] = df_f['text_lower'].str.replace(r'\s+', ' ', regex=True).str.strip()
print(df_f['text_lower'].head(20))



# удаляем пунктуацию
translator = str.maketrans('', '', '.,!?:;-()[]{}"""\'…—«»')
#apply - запускает цикл и обрабатывает каждую строчку, lambda x - функция, где х -текст конкретного отзыва
df_f['text_lower'] = df_f['text_lower'].astype(str).apply(lambda x: x.translate(translator))
df_f['text_lower'].head(20)


#                Удаление стоп-слов
#Импорт стоп-слов из бибилиотеки nltk
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('russian'))

# функция, удаляющая стопслова из текстов
def remove_stopwords(text):
    return " ".join([word for word in text.split() if word not in STOPWORDS])
# Применим функцию удаления стоп-слов
df_f["text_lower"] = df_f["text_lower"].apply(remove_stopwords)
df_f["text_lower"].head()


#Удаление высокочастотных слов
from collections import Counter
cnt = Counter()
for text in df_f["text_lower"].values:
    for word in text.split():
        cnt[word] += 1
        
print("20 частых слов: ", cnt.most_common(10))
print("\nПервые строки датасета: ")
print(df_f[['text', 'text_lower']].head())

# удаление часто встречающиеся слов в корпусе при помощи tf-idf
# Удаление самых частотных слов
freq = set([w for (w, wc) in cnt.most_common(10)])
# функция удаления слов
def freqwords(text):
    return " ".join([word for word in str(text).split() if word not 
in freq])
# применение функции
df_f["text_lower"] = df_f["text_lower"].apply(freqwords)
df_f["text_lower"].head()


#Удаление низкочастотных слов
freq = pd.Series(' '.join(df_f['text_lower']).split()).value_counts()[-10:] # 10 rare words
freq = list(freq.index)
print(freq)
df_f['text_lower'] = df_f['text_lower'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
df_f['text_lower'].head()

# Удаление эмодзи
def emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
#passing the emoji function to 'text_rare'
df_f['text_lower'] = df_f['text_lower'].apply(emoji)


#Токенизация
def tokenization(text):
    return [word for word in str(text).split() if word]
# Passing the function to 'text_rare' and store into'text_token'
df_f['ready'] = df_f['text_lower'].apply(tokenization)
# print(df_f[['ready']].head())


# Лемматизация

from pymorphy3 import MorphAnalyzer
from nltk import sent_tokenize, word_tokenize, regexp_tokenize

def tokenize_lemmas(sent, pat=r"(?u)\b\w\w+\b", morph=MorphAnalyzer()):
    return [morph.parse(tok)[0].normal_form 
            for tok in regexp_tokenize(sent, pat)]
df_f["text_lower"] = df_f["text_lower"].map(lambda x: " ".join(tokenize_lemmas(x)))
print(df_f[['text_lower']].head())

df_f.to_csv("reviews_prep.csv", encoding="UTF-8", index = False)