import re
import sys
from pymystem3 import Mystem
import pandas as pd
import numpy as np
from sklearn.metrics import adjusted_rand_score
import tqdm
import gensim
#print('\n'.join(f'{m.__name__}=={m.__version__}' for m in globals().values() if getattr(m, '__version__', None))) # с помощью globals() создадим спецсловарь 
# и вернем оттуда только объекты values, затем проверкой getattr оставим только библиотеки, проверив на наличие версии, и выведем их название и версию

from gensim.utils import tokenize
from gensim import utils
from gensim.test.utils import datapath
from gensim.models import Word2Vec
#print('\n'.join(f'{m.__name__}=={m.__version__}' for m in globals().values() if getattr(m, '__version__', None)))

from gensim.test.utils import common_texts  # some example sentences
dataset = open("zamok.test", "r", encoding = 'UTF-8') # считываем датасет и строки в нем, аргумент 'r' помогает открывать файл только для чтения
lines = dataset.readlines() # возвращает список строк, в конце каждой строки символ переноса

dataset = [s.split() for s in lines] # .split() без параметров разрезает текстовую строку по пробелам на отдельные слова и создается список списков строк
#print(dataset)
class MyIter: # объявление класса-итератора для эффективного чтения данных
    def __iter__(self): # определение спец метода для итерации объекта в цикле
        for line in lines: # построчный обход ранее считанного массива строк
            yield line.split() # выдача строки, разбитой на отдельные слова по пробелам. yield здесь вместо return, он позволяет генерировать списки слов только по запросу 
model4 = Word2Vec(vector_size=6, window=3, min_count=1, sg = 0) # создаём саму структуру нейросети и настраиваем гиперпараметры:
# размер эмбеддинга=6, размер контекстного окна=3 слова, минимальная частота слова в тексте=1(берем все слова), выбор алгоритма обучения=0 (CBOW)
model4.build_vocab(corpus_iterable=MyIter()) # модель читает весь текст, подсчитывает сколько раз оно встретилось и создает внутр.словарь, происходит
# присвоение каждого слова начального случайного вектора из 6 чисел
total_examples = model4.corpus_count # обращаемся к только что построенному словарю модели, чтобы узнать точное количество строк
model4.train(corpus_iterable=MyIter(), total_examples=total_examples, epochs=6) #запускс процесса обучения. corpus_iterable=MyIter()-указывает модели источник данных для обучения
#total_examples передаёт модели точное количество предложений для регулировки скорости обучения и равномерного распределения нагрузки
# количество эпох (полных циклов обучения) 6
#print(model4.wv.most_similar(positive=['замо`к'], topn=30))
#print(model4.wv.most_similar(positive=['за`мок'], topn=30))
#print(model4.wv.most_similar_to_given(["атаку"], ["за`мок", "замо`к"]))
model4.save("word2vec_zamok.model")