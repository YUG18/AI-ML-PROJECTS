# 🧠 Fake News Detector

Hey there!  
This is a simple ML project I built to detect whether a news article is fake or real.  
I used a dataset from Kaggle containing real and fake news headlines + content.

## 🚀 What it Does
- Cleans the text data using NLP techniques
- Converts text into numerical vectors using TF-IDF
- Trains a Logistic Regression model to classify news as Real or Fake
- Includes `.pkl` files to directly use the trained model

## 🧠 Tech Used
- Python
- Pandas, Numpy
- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression

## 📊 Dataset
> Note: Dataset is quite large (~110MB in total), so you might face GitHub LFS warnings.

If you want to test it yourself, download the dataset from here:  
[Kaggle Dataset - Fake and Real News](https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset)

## 🧪 How to Run
1. Install the dependencies
```bash
pip install -r requirements.txt
