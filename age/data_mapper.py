import pandas as pd
import os

from reader.excel_reader import ExcelReader

# card_id 열의 데이터를 고유한 숫자로 매핑

class DataMapper:
    def __init__(self, df, column_name):
        self.column_name = column_name
        self.df = df
        self.card_mapping = {}
        self.next_index = 0

    def map_data(self, data):
        if data not in self.card_mapping:
            self.card_mapping[data] = self.next_index
            self.next_index += 1
        return self.card_mapping[data]

    def apply_mapping(self):
        if self.column_name not in self.df.columns:
            raise ValueError(f"'{self.column_name}' column not found in DataFrame.")

        self.df[self.column_name] = self.df[self.column_name].map(self.map_data)


if __name__ == "__main__":
    script_directory = os.path.dirname(__file__)
    print("project_importer script_directory: ", script_directory)

    file_path = "../data/chunk_1-5000.xlsx"
    absolute_file_path = os.path.abspath(os.path.join(script_directory, file_path))
    print("absolute_file_path: ", absolute_file_path)

    reader_xlsx = ExcelReader(absolute_file_path)
    df = reader_xlsx.read_file()
    if df is not None:
        columns = reader_xlsx.get_columns()
        if columns is not None and 'card_id' in columns:
            column_name = 'card_id'
            data_mapper = DataMapper(df, column_name)

            try:
                data_mapper.apply_mapping()
            except ValueError as e:
                print(e)

            print(data_mapper.card_mapping)
            # print(df)
        else:
            print("'card_id' column not found in DataFrame.")
    else:
        print("DataFrame is empty.")
