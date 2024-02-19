import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report
class Model:
    svm = SVC(kernel='linear')
    vectorizer = CountVectorizer()
    def predictive_function(self,str):
        new_predict = self.svm.predict(str)
        return new_predict
    def vectorize_values(self,str):
        new_features = self.vectorizer.transform(str)
        return new_features
    def __init__(self):
        data = pd.read_csv("C:\\Users\\mohamed irfaan\\Downloads\\emotions\\EcoPreprocessed.csv")
        text = data['review'].values
        labels = data['division'].values
        text_train, text_test, labels_train, labels_test = train_test_split(text, labels, test_size=0.2, random_state=42)
        
        features_train = self.vectorizer.fit_transform(text_train)
        features_test = self.vectorize_values(text_test)
        self.svm.fit(features_train, labels_train)
        predictions = self.predictive_function(features_test)
        new_text = ["I love this movie!", "This product is terrible.", "The food was delicious."]
        new_features = self.vectorize_values(new_text)
        new_predictions = self.predictive_function(new_features)
        print(new_predictions)
        from sklearn.metrics import accuracy_score
        self.accuracy = accuracy_score(labels_test, predictions)
        print(accuracy_score(labels_test, predictions))
        from sklearn.metrics import mean_squared_error,classification_report,confusion_matrix,accuracy_score
        print(classification_report(labels_test,predictions))
        print(confusion_matrix(labels_test,predictions))

model = Model()