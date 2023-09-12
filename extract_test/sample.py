import os
from extractor.excel_extractor import ExcelExtractor

if __name__ == "__main__":
    script_directory = os.path.dirname(__file__)
    print("project_importer script_directory: ", script_directory)

    file_path = "../data/add_card_data.csv"
    absolute_file_path = os.path.abspath(os.path.join(script_directory, file_path))
    print("absolute_file_path: ", absolute_file_path)

    separate_range = 5000
    total_rows = 50000

    extractor = ExcelExtractor(absolute_file_path, separate_range, total_rows)
    output_format = "excel"
    extractor.extract_excel_chunks(output_format)