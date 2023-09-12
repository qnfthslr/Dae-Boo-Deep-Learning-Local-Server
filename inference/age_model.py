import os
import numpy as np
from keras.models import load_model
from tensorflow import keras

from deep_learn.age.learning_processor import AgeBasedLearningProcessor

if __name__ == "__main__":
    loaded_model = load_model(os.path.join("../data/model", 'age_based_card_recommand.h5'))

    columns = ['연령대별', '카드 번호']
    output_names = ['age_map_data.xlsx', 'card_number_map_data.xlsx']
    learning_processor = AgeBasedLearningProcessor(columns, output_names)

    learning_processor.set_file_path('../data/chunk_1-5000.xlsx')
    request_columns_map_data, dataframe = learning_processor.make_map_data_to_excel()

    X_data = dataframe[columns[0]].map(request_columns_map_data[0])
    y_data = dataframe[columns[1]].replace(request_columns_map_data[1])
    X = X_data.values
    y = y_data.values

    # encoded_age_type = \
    #     keras.utils.to_categorical(X,
    #         num_classes=len(request_columns_map_data[0]))
    # encoded_card_number_type = \
    #     keras.utils.to_categorical(y,
    #         num_classes=len(request_columns_map_data[1]))

    print(f"request_columns_map_data[0].values(): {request_columns_map_data[0].values()}")
    print(f"request_columns_map_data[1].values(): {request_columns_map_data[1].values()}")

    age_predictions = loaded_model.predict(X)
    print(f"age_predictions: {age_predictions}")
    predicted_age_index = np.argmax(age_predictions)
    print(f"predicted_age_index: {predicted_age_index}")
    #predicted_age = request_columns_map_data[0][predicted_age_index]

    age_data = np.array([request_columns_map_data[0]['20대']])
    predicted_probs = loaded_model.predict(age_data)[0]
    recommended_card_indices = np.argsort(predicted_probs)[::-1][:5]
    recommended_card_numbers = [list(request_columns_map_data[1].keys())[i] for i in recommended_card_indices]
    print(f"recommended_card_numbers: {recommended_card_numbers}")

