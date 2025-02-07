import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
import csv

# todo o csv e passa para a varivale base_treinamento
with open('C:/Users/ti.joao/Documents/GitHub/Real_Estate/input/treinamento.csv', newline='') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')

    base_treinamento = [tuple(row) for row in reader]

    #print(base_treinamento)

#cria um data frame para adicionar as colunas
data = pd.DataFrame(base_treinamento)
data.columns = ['Frase', 'Sentimento']

#mapeia todas os sentimentos e depois compara e troca os nomes por valores
mapping = {'alegria': 0, 'neutro': 1, 'tristeza': 2, 'raiva': 3}
data['Sentimento'] = data['Sentimento'].map(mapping)

#pega os values das frases e sentiementos
texts = data['Frase'].values
labels = data['Sentimento'].values

#faz a tokenização das frases
tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

#A PARTIR DAQUI PODE COMENTAR PARA QUANDO NÃO FOR TREINAR
padded_sequences = pad_sequences(sequences, maxlen=100, truncating='post', padding='post')

training_size = int(len(padded_sequences) * 0.8)
training_sequences = padded_sequences[:training_size]
training_labels = labels[:training_size]

testing_sequences = padded_sequences[training_size:]
testing_labels = labels[training_size:]

model = Sequential([
    Embedding(10000, 64),
    Bidirectional(LSTM(64)),
    Dense(64, activation='relu'),
    Dense(4, activation='softmax')
])

# compila e executa todo o treinamento e testa
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(
    training_sequences,
    training_labels,
    epochs=10,
    validation_data=(testing_sequences, testing_labels)
)

# salva o modelo com esse nome
# model.save('baxacinho.0.1')

# aqui faz o teste e calcula a acuracia do modelo
test_loss, test_acc = model.evaluate(testing_sequences, testing_labels)
print('Test Accuracy:', test_acc)

#NÃO COMENTAR ESSA FUNÇÃO
def sentimento(alegria, raiva, tristeza, neutro):
    if alegria > raiva and alegria > tristeza and alegria > neutro:
        print('O sentimento que está sentido é alegria')

    elif raiva > alegria and raiva > tristeza and raiva > neutro:
        print('O sentimento que está sentido é raiva')

    elif tristeza > alegria and tristeza > raiva and tristeza > neutro:
        print('O sentimento que está sentido é tristeza')

    elif neutro > alegria and neutro > raiva and neutro > tristeza:
        print('O sentimento que está sentido é neutro')

    else:
        print('O sentimento não encontrado')

