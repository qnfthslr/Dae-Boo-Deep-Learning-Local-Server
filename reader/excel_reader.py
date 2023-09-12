import pandas as pd
import os

class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[-1].lower()
        self.df = None

    def read_file(self):
        try:
            if self.file_extension == ".xlsx":
                self.df = pd.read_excel(self.file_path)
            elif self.file_extension == ".csv":
                self.df = pd.read_csv(self.file_path)
            else:
                print("Unsupported file format:", self.file_extension)
                return None

            return self.df

        except Exception as e:
            print(f"Error reading file: {e}")
            return None

    def get_columns(self):
        if self.df is not None:
            return self.df.columns.tolist()
        else:
            return None


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
        if columns is not None:
            print("Columns in DataFrame:")
            print(columns)
        else:
            print("DataFrame is empty.")

    print(df)
