import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

def train_model():
    # Load fake and true news datasets
    fake_news = pd.read_csv("./BackEnd/Datasets/fake.csv")
    true_news = pd.read_csv("./BackEnd/Datasets/true.csv")

    # Add a label column to distinguish fake (1) and true (0) news
    fake_news["label"] = 1
    true_news["label"] = 0

    # Combine title, subject, and text fields into a single field
    fake_news["combined_text"] = (
        fake_news["title"] + " " + fake_news["subject"] + " " + fake_news["text"]
    )
    true_news["combined_text"] = (
        true_news["title"] + " " + true_news["subject"] + " " + true_news["text"]
    )

    # Select important fields for classification
    data = pd.concat(
        [fake_news[["combined_text", "label"]], true_news[["combined_text", "label"]]]
    )

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        data["combined_text"], data["label"], test_size=0.2, random_state=42
    )

    # Preprocess text and convert it to TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Initialize and train the Logistic Regression (Softmax) model
    model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000)
    model.fit(X_train_tfidf, y_train)

    # Calculate accuracy
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)

    return model, vectorizer, accuracy

def save_model(model, vectorizer, accuracy):
    # Save the model and vectorizer to files
    joblib.dump(model, './BackEnd/Models/Normal/SoftMax/softmax_model.pkl')
    joblib.dump(vectorizer, './BackEnd/Models/Normal/Softmax/softMax_vectorizer.pkl')

    # Export accuracy to a file
    with open('./BackEnd/AccuracyData/algorithm_accuracy_normal.txt', 'a') as f:
        f.write(f"\nSoftMax - {accuracy}\n")

# Call the functions
model, vectorizer, accuracy = train_model()
save_model(model, vectorizer, accuracy)
