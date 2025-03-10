import os

from age.data_mapper import DataMapper
from reader.excel_reader import ExcelReader

# excel 일겅와서 열의 데이터를 매핑

class DataMappingProcessor:
    def __init__(self, file_path, column_name):
        self.file_path = file_path
        self.column_name = column_name
        self.df = None

    def process_mapping(self):
        script_directory = os.path.dirname(__file__)
        print("project_importer script_directory: ", script_directory)

        absolute_file_path = os.path.abspath(os.path.join(script_directory, self.file_path))
        print("absolute_file_path: ", absolute_file_path)

        reader_xlsx = ExcelReader(absolute_file_path)
        self.df = reader_xlsx.read_file()
        if self.df is not None:
            columns = reader_xlsx.get_columns()
            if columns is not None and self.column_name in columns:
                data_mapper = DataMapper(self.df, self.column_name)

                try:
                    data_mapper.apply_mapping()
                except ValueError as e:
                    print(e)

                print(data_mapper.card_mapping)
                return data_mapper.card_mapping
            else:
                print(f"'{self.column_name}' column not found in DataFrame.")
        else:
            print("DataFrame is empty.")

    def set_column_name(self, new_column_name):
        self.column_name = new_column_name

    def get_dataframe(self):
        return self.df


if __name__ == "__main__":
    file_path = "../data/chunk_1-5000.xlsx"

    column_name = 'card_id'
    data_mapping_processor = DataMappingProcessor(file_path, column_name)
    data_mapping_processor.process_mapping()

    data_mapping_processor.set_column_name('age')
    data_mapping_processor.process_mapping()
