import json


class Utils:

    @classmethod
    def json_to_string(cls, json_information):
        """
        Convert object json to string.
        :param json_information: The object that convert to string
        :return: json string or None with errors.
        """
        try:
            json_str = json.dumps(json_information._json)
            return json_str
        except json.JSONDecodeError as e:
            print("[json_to_string] Error " + str(e))

        return None

    @classmethod
    def get_json_output(cls, file_name, dataset_directory, item):
        """
        Generate a json file from user information. If the file exists, append new item.
        :return: a new json file, or a new item
        """
        # file_name = 'user_file.json'
        path_file = dataset_directory + '/' + file_name
        #with open(path_file, mode='a+', encoding='utf8') as user_file:
        with open(path_file, mode='a+') as user_file:
            json.dump(item, user_file, indent=4) # indent=4 nos formatea la salida del texto.

