import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()

model = load_model('model/chatbot_model.h5')
intents = json.loads(open('data/intents.json', encoding='utf-8').read())
words = pickle.load(open('model/words.pkl', 'rb'))
classes = pickle.load(open('model/classes.pkl', 'rb'))

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]

def get_response(intents_list, intents_json):
    if len(intents_list) == 0:
        return "Desculpe, não entendi. Pode repetir?"
    tag = intents_list[0]['intent']
    for intent in intents_json['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])
    return "Desculpe, não entendi. Pode repetir?"

def chatbot_response(msg):
    ints = predict_class(msg)
    return get_response(ints, intents)

if __name__ == "__main__":
    print("🤖 Chatbot do Edu iniciado! Digite 'sair' para encerrar.")
    while True:
        msg = input("Você: ")
        if msg.lower() == "sair":
            break
        res = chatbot_response(msg)
        print("Bot:", res)