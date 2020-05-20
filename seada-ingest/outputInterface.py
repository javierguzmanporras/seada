class OutputInterface:

    def get_csv_output(self, file_name: str, dataset_directory: str):
        """Generate a csv file from item information. If the file exists, append new line."""
        pass

    def get_json_output(self, file_name: str, dataset_directory: str):
        """Generate a json file from item information. If the file exists, append new item."""
        pass

    def get_tuple_output(self) -> tuple:
        """Generate a tuple type with item information for input into a database"""
        pass

