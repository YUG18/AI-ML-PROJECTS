import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
#To make the text free from impurities if content is scraped from web browsers
def clean_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text) #removes HTML contents
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # remove URLs
    text = re.sub(r'[^a-z\s]', '', text)  # remove non-alphabetic characters
    return text
#Make tables for fake and true news
fake = pd.read_csv("Fake.csv").head(200)
true = pd.read_csv("True.csv").head(200)
#add a column label
fake["label"] = "FAKE"
true["label"] = "TRUE"
#merge them into single table
data = pd.concat([fake,true])
#shuffle the data table
data = data.sample(frac=1).reset_index(drop=True)
data['clean_text']=data['text'].apply(clean_text)
X = data['clean_text']
Y = data['label']
#converts text into numeric features
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
#stop words removes words like 'is' , 'and' , 'the'
#max_df is used to remove words which repeat more than 70% in text
X_vectors = vectorizer.fit_transform(X)
X_train,X_test,Y_train,Y_test = train_test_split(X_vectors,Y,test_size=0.2,random_state=42)
model = PassiveAggressiveClassifier(max_iter=1000) #for classification process
model.fit(X_train,Y_train)
y_predict = model.predict(X_test)
accuracy = accuracy_score(Y_test,y_predict)
print("Classification Report")
print(classification_report(Y_test,y_predict))
print("Confusion Report")
print(confusion_matrix(Y_test,y_predict))
print(f"Accuracy of model is {round(accuracy*100),2}%")
joblib.dump(model,"model.pkl")
joblib.dump(vectorizer,"vectorizer.pkl")
print("Model and vectorizer saved as model.pkl and vectorizer.pkl")
if __name__=="__main__":
    while True:
        print("Enter the article text or 'exit' to break out")
        user_input = input(">>  ")
        if user_input.lower() =='exit':
            break
        cleaned_input = clean_text(user_input)
        user_vector = vectorizer.transform([cleaned_input])
        prediction = model.predict(user_vector)[0]
        print("Prediction : ",prediction)