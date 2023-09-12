import os

from mapper.data_mapping_processor import DataMappingProcessor
from writer.excel_writer import ExcelWriter


class AgeBasedLearningProcessor:
    def __init__(self, columns, output_file_names):
        if len(columns) != len(output_file_names):
            raise ValueError("The lengths of 'columns' and 'output_file_names' must be the same.")

        self.request_columns = columns
        self.analysis_file_names = output_file_names
        self.output_dir = "../data/intermediate"
        self.file_path = None
        self.process_loop_count = len(columns)

    def make_learning_data(self, file_path):
        self.file_path = file_path

        request_columns_map_data = self.make_map_data_to_excel()

    def make_map_data_to_excel(self):
        request_columns_map_data = []

        for idx in range(self.process_loop_count):
            data_mapping_processor = DataMappingProcessor(self.file_path, self.request_columns[idx])
            columns_map_data = data_mapping_processor.process_mapping()
            request_columns_map_data.append(columns_map_data)

            excel_writer = ExcelWriter(self.output_dir)
            print(f"analysis_file: {self.analysis_file_names[idx]}")
            excel_writer.write_to_excel(self.analysis_file_names[idx], columns_map_data)

        return request_columns_map_data


if __name__ == "__main__":
    columns = ['연령대별', '카드 번호']
    output_names = ['age_map_data.xlsx', 'card_number_map_data.xlsx']
    file_path_for_read = '../data/chunk_1-5000.xlsx'
    learning_processor = AgeBasedLearningProcessor(columns, output_names)

    learning_processor.make_learning_data(file_path_for_read)

