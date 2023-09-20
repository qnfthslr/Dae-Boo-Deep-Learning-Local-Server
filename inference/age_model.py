import os
import numpy as np
from keras.models import load_model
from tensorflow import keras
from deep_learn.age.learning_processor import AgeBasedLearningProcessor

class AgeBasedinferringProcessor:
    def __init__(self):
        self.loaded_model = load_model(os.path.join("./data/model", 'age_based_card_recommand.h5'))
        self.columns = ['age', 'card_id']
        self.output_names = ['age_map_data.xlsx', 'card_number_map_data.xlsx']
        self.learning_processor = AgeBasedLearningProcessor(self.columns, self.output_names)

    def process_data(self, file_path):
        self.learning_processor.set_file_path(file_path)
        request_columns_map_data, dataframe = self.learning_processor.make_map_data_to_excel()

        X_data = dataframe[self.columns[0]].map(request_columns_map_data[0])
        y_data = dataframe[self.columns[1]].replace(request_columns_map_data[1])
        X = X_data.values
        y = y_data.values

        age_predictions = self.loaded_model.predict(X)
        print(f"age_predictions: {age_predictions}")
        predicted_age_index = np.argmax(age_predictions)
        print(f"predicted_age_index: {predicted_age_index}")

        age_data = np.array([request_columns_map_data[0][20]])
        predicted_probs = self.loaded_model.predict(age_data)[0]
        recommended_card_indices = np.argsort(predicted_probs)[::-1][:5]
        recommended_card_numbers = [list(request_columns_map_data[1].keys())[i] for i in recommended_card_indices]
        print(f"recommended_card_numbers: {recommended_card_numbers}")

        age_data = np.array([request_columns_map_data[0][30]])
        predicted_probs = self.loaded_model.predict(age_data)[0]
        recommended_card_indices = np.argsort(predicted_probs)[::-1][:5]
        recommended_card_numbers = [list(request_columns_map_data[1].keys())[i] for i in recommended_card_indices]
        print(f"recommended_card_numbers: {recommended_card_numbers}")

        return 1

if __name__ == "__main__":
    processor = AgeBasedinferringProcessor()
    processor.process_data('../data/chunk_1-5000.xlsx')
