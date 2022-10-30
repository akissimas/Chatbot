import pandas as pd
import neattext.functions as nfx

# machine learning packages
# Estimators
from sklearn.linear_model import LogisticRegression

# Transformers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

# Build Pipeline
from sklearn.pipeline import Pipeline


class Emotion:
    def __init__(self):
        self.dataset = None
        self.ylabels = None
        self.Xfeatures = None
        self.pipe_lr = None
        self.y_test = None
        self.y_train = None
        self.x_test = None
        self.x_train = None

    def read_dataset(self):
        train_dataset = pd.read_csv("./dataset/train.csv")
        test_dataset = pd.read_csv("./dataset/test.csv")
        valid_dataset = pd.read_csv("./dataset/val.csv")

        list_dataset = [train_dataset, test_dataset, valid_dataset]

        self.dataset = pd.concat(list_dataset)

        # remove stopwords
        self.dataset['Text'] = self.dataset['Text'].apply(nfx.remove_stopwords)

        self.Xfeatures = self.dataset['Text']
        self.ylabels = self.dataset['Emotion']

    def train_model(self):
        #  Split Data
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.Xfeatures, self.ylabels, test_size=0.3, random_state=42)

        # LogisticRegression Pipeline
        self.pipe_lr = Pipeline(steps=[('cv', CountVectorizer()), ('lr', LogisticRegression())])

        # Train and Fit Data
        self.pipe_lr.fit(self.x_train, self.y_train)


    def check_accuracy(self):
        # Check Accuracy
        return self.pipe_lr.score(self.x_test, self.y_test)

    def prediction(self, text):
        return self.pipe_lr.predict([text])


if __name__ == '__main__':
    emotion = Emotion()

    emotion.read_dataset()

    emotion.train_model()

    # Make A Prediction
    sample = "I have to look at life in her perspective, and it would break anyone’s heart.", \
             "We stayed in a tiny mountain village called Droushia, and these people brought hospitality to incredible new heights.", \
             "But the rest of it came across as a really angry, drunken rant.", \
             "Which, to be honest, was making Brad slightly nervous."

    print(f"check accuracy: {emotion.check_accuracy()}\n")

    # print(f"prediction: {emotion.pipe_lr.predict(emotion.x_test.real)}\n")
    print(f"prediction: {emotion.pipe_lr.predict(sample)}")

