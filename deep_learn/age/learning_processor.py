import os

from mapper.data_mapping_processor import DataMappingProcessor
from writer.excel_writer import ExcelWriter

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

import numpy as np


class AgeBasedLearningProcessor:
    def __init__(self, columns, output_file_names):
        if len(columns) != len(output_file_names):
            raise ValueError("The lengths of 'columns' and 'output_file_names' must be the same.")

        self.request_columns = columns
        self.analysis_file_names = output_file_names
        self.output_dir = "../data/intermediate"
        self.learning_output_dir = "../../data/model"
        self.file_path = None
        self.process_loop_count = len(columns)

    def make_learning_data(self, file_path):
        self.file_path = file_path

        request_columns_map_data, dataframe = self.make_map_data_to_excel()
        #df_list = self.make_map_data_to_excel()

        # TODO: 컬럼의 X, Y가 잘 명시되지 않고 있음
        #       추후 Refactoring이 필요한 부분임
        print(f"map_data: {request_columns_map_data[0]}")
        print(f"map_data: {request_columns_map_data[1]}")

        X_data = dataframe[self.request_columns[0]].map(request_columns_map_data[0])
        print("X_data: ", X_data)
        print("X_data type: ", type(X_data))

        print("dataframe['카드 번호']: ", dataframe[self.request_columns[1]])
        print("request_columns_map_data[1]: ", request_columns_map_data[1])

        y_data = dataframe[self.request_columns[1]].replace(request_columns_map_data[1])
        print("y_data: ", y_data)
        print(f"y_data type: {type(y_data)}")

        X = X_data.values
        y = y_data.values
        print("X: ", X)
        print("y: ", y)
        print(f"len(card_mapping): {len(request_columns_map_data[1])}")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Sequential()
        model.add(Dense(64, input_dim=1, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(len(request_columns_map_data[1]), activation='softmax'))

        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # 모델 훈련
        model.fit(X_train, y_train, epochs=10, batch_size=8, verbose=1)

        model.save(os.path.join(self.learning_output_dir, 'age_based_card_recommand.h5'))


    def make_map_data_to_excel(self):
        request_columns_map_data = []

        data_mapping_processor = None
        for idx in range(self.process_loop_count):
            data_mapping_processor = DataMappingProcessor(self.file_path, self.request_columns[idx])
            columns_map_data = data_mapping_processor.process_mapping()
            request_columns_map_data.append(columns_map_data)

            excel_writer = ExcelWriter(self.output_dir)
            print(f"analysis_file: {self.analysis_file_names[idx]}")
            excel_writer.write_to_excel(self.analysis_file_names[idx], columns_map_data)

        df = data_mapping_processor.get_dataframe()
        return request_columns_map_data, df


if __name__ == "__main__":
    columns = ['연령대별', '카드 번호']
    output_names = ['age_map_data.xlsx', 'card_number_map_data.xlsx']
    file_path_for_read = '../data/chunk_1-5000.xlsx'
    learning_processor = AgeBasedLearningProcessor(columns, output_names)

    learning_processor.make_learning_data(file_path_for_read)

