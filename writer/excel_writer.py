import os
import pandas as pd

from mapper.data_mapping_processor import DataMappingProcessor


class ExcelWriter:
    def __init__(self, target_directory):
        script_directory = os.path.dirname(__file__)
        print("project_importer script_directory: ", script_directory)

        absolute_file_path = os.path.abspath(os.path.join(script_directory, target_directory))
        print("absolute_file_path: ", absolute_file_path)

        self.output_directory = absolute_file_path

    def write_to_excel(self, file_name, data_mapping):
        # 데이터 매핑을 DataFrame으로 변환
        df = pd.DataFrame(data_mapping.items(), columns=['Value', 'MappedValue'])

        # Excel 파일로 저장
        excel_file_path = os.path.join(self.output_directory, file_name)
        df.to_excel(excel_file_path, index=False)

    def write_to_csv(self, file_name, data_mapping):
        # 데이터 매핑을 DataFrame으로 변환
        df = pd.DataFrame(data_mapping.items(), columns=['Value', 'MappedValue'])

        # CSV 파일로 저장
        csv_file_path = os.path.join(self.output_directory, file_name)
        df.to_csv(csv_file_path, index=False)


if __name__ == "__main__":
    virtual_mapping = {'40대': 0, '30대': 1, '50대': 2, '70대이상': 3, '20대': 4, '60대': 5, '10대': 6}

    output_directory = "../data/intermediate"

    excel_output_file = "virtual_mapping.xlsx"
    excel_writer = ExcelWriter(output_directory)
    excel_writer.write_to_excel(excel_output_file, virtual_mapping)

    print(
        f"Data mapping saved to '{os.path.join(output_directory, excel_output_file)}' (Excel)")

    file_path = "../data/chunk_1-5000.xlsx"

    column_name = 'card_id'
    data_mapping_processor = DataMappingProcessor(file_path, column_name)
    map_data = data_mapping_processor.process_mapping()

    analysis_data_file = "card_map_result.xlsx"
    excel_writer = ExcelWriter(output_directory)
    excel_writer.write_to_excel(analysis_data_file, map_data)
