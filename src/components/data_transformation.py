import re
import string
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def preprocess_text(self, text):
        # Replace special characters and punctuation with a blank space
        pattern_special_chars = r'[^\w\s]'
        text = re.sub(pattern_special_chars, ' ', text)

        # Convert the text to lowercase
        text = text.lower()

        return text

    def filter_short_messages(self, df):
        return df[df['Received'].str.len() > 5]

    def drop_columns(self, df):
        return df.drop(['Message', 'Phone Number'], axis=1)

    def tfidf_vectorizer(self, received_messages):
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(received_messages)
        return tfidf_matrix

    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            logging.info("Entered the data transformation method or component")

            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)

            logging.info("Applying preprocessing object on training and testing dataframes.")

            train_df['Received'] = train_df['Received'].apply(self.preprocess_text)
            train_df = self.filter_short_messages(train_df)
            train_df = self.drop_columns(train_df)

            test_df['Received'] = test_df['Received'].apply(self.preprocess_text)
            test_df = self.filter_short_messages(test_df)
            test_df = self.drop_columns(test_df)

            logging.info("TF-IDF Vectorization.")
            train_arr = self.tfidf_vectorizer(train_df['Received'])
            test_arr = self.tfidf_vectorizer(test_df['Received'])

            logging.info("Saved preprocessing object.")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=self  # Save the DataTransformation instance itself
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)



