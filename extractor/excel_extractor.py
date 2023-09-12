import pandas as pd
import os

class ExcelExtractor:
    def __init__(self, file, separate_range, total_rows):
        self.file = file
        self.separate_range = separate_range
        self.total_rows = total_rows

        current_directory = os.path.dirname(__file__)
        print("project_importer script_directory: ", current_directory)

        dir_path = "../data"
        absolute_dir_path = os.path.abspath(os.path.join(current_directory, dir_path))
        print("absolute_file_path: ", absolute_dir_path)

        self.output_dir = absolute_dir_path

        detected_file_format = self.detect_file_format(file)

        if "xlsx" == detected_file_format:
            self.df = pd.read_excel(file)
        elif "csv" == detected_file_format:
            self.df = pd.read_csv(file)
        else:
            print("형식이 잘못되었습니다!")

    def detect_file_format(self, file_path):
        file_extension = os.path.splitext(file_path)[-1].lower()

        if file_extension == ".xlsx":
            return "xlsx"
        elif file_extension == ".csv":
            return "csv"
        else:
            return None

    def extract_excel_chunks(self, output_format="excel"):
        for i in range(0, self.total_rows, self.separate_range):
            start_row = i
            end_row = min(i + self.separate_range, self.total_rows)
            chunk = self.df[start_row:end_row]

            if output_format == "excel":
                file_name = f'chunk_{start_row + 1}-{end_row}.xlsx'
            elif output_format == "csv":
                file_name = f'chunk_{start_row + 1}-{end_row}.csv'
            else:
                print("Unsupported output format:", output_format)
                return

            target_file_path = os.path.join(self.output_dir, file_name)

            if output_format == "excel":
                chunk.to_excel(target_file_path, index=False)
            elif output_format == "csv":
                chunk.to_csv(target_file_path, index=False)

            print(f"Extracted chunk {start_row + 1}-{end_row} to {output_format} file.")


if __name__ == "__main__":
    script_directory = os.path.dirname(__file__)
    print("project_importer script_directory: ", script_directory)

    file_path = "../data/add_card_data.csv"
    absolute_file_path = os.path.abspath(os.path.join(script_directory, file_path))
    print("absolute_file_path: ", absolute_file_path)

    separate_range = 100
    total_rows = 500

    extractor = ExcelExtractor(absolute_file_path, separate_range, total_rows)
    output_format = "excel"
    extractor.extract_excel_chunks(output_format)
