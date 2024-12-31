import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer # type: ignore
from tensorflow.keras.preprocessing.sequence import pad_sequences  # type: ignore
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Embedding, LSTM, Dense  # type: ignore
import joblib

def train_model():
    # Load data
    fake_news = pd.read_csv("./BackEnd/Datasets/fake.csv")
    true_news = pd.read_csv("./BackEnd/Datasets/true.csv")

    # Combine title, subject, and text fields into one
    fake_news["combined_text"] = fake_news["title"] + " " + fake_news["subject"] + " " + fake_news["text"]
    true_news["combined_text"] = true_news["title"] + " " + true_news["subject"] + " " + true_news["text"]

    # Assign labels to the data
    fake_news["label"] = 1
    true_news["label"] = 0

    # Select relevant fields for classification
    data = pd.concat([fake_news[["combined_text", "label"]], true_news[["combined_text", "label"]]])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data["combined_text"], data["label"], test_size=0.2, random_state=42)

    # Tokenize text
    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(X_train)
    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    # Pad sequences to uniform length
    max_length = 100
    X_train_padded = pad_sequences(X_train_seq, maxlen=max_length)
    X_test_padded = pad_sequences(X_test_seq, maxlen=max_length)

    # Build LSTM model
    model = Sequential()
    model.add(Embedding(10000, 128, input_length=max_length))
    model.add(LSTM(64))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    history = model.fit(X_train_padded, y_train, epochs=10, batch_size=32, validation_data=(X_test_padded, y_test))

    # Get accuracy from history
    accuracy = history.history['val_accuracy'][-1]

    return model, tokenizer, accuracy

def save_model(model, tokenizer, accuracy):
    # Save model architecture and weights
    model.save('./BackEnd/Models/Normal/LSTM/lstm_model.keras')

    # Save tokenizer
    with open('./BackEnd/Models/Normal/LSTM/lstm_tokenizer.pkl', 'wb') as handle:
        joblib.dump(tokenizer, handle)

    # Export accuracy to a file
    with open('./BackEnd/AccuracyData/algorithm_accuracy_normal.txt', 'a') as f:
        f.write(f"\nLSTM - {accuracy}\n")    

# Train model and save
model, tokenizer, accuracy = train_model()
save_model(model, tokenizer, accuracy)
