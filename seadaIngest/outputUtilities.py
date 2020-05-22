import csv
import json
import logging


class OutputUtilities:
    """Common json and csv utilities"""

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
    def get_json_output(cls, file_name, dataset_directory, item, datatag='data_list'):
        """
        Generate a json file from item information. If the file exists, append new item.
        :return: a new json file, or a new item
        """
        path_file = dataset_directory + '/' + file_name
        try:
            with open(path_file) as json_file:
                data_temp = json.load(json_file)
                list_temp = data_temp[datatag]
                list_temp.append(item)
                data = {datatag: list_temp}
        except IOError:
            logging.warning('[outputUtilities.get_json_output] IOError: File json not exits')
            data_list = [item]
            data = {datatag: data_list}
        except Exception as exception:
            print('[+] Error: {}'.format(exception))
            logging.exception('[outputUtilities.get_json_output] Error with json files: {}'.format(exception))

        with open(path_file, mode='w', encoding='utf8') as user_file:
            try:
                json.dump(data, user_file, indent=4, ensure_ascii=False)  # indent=4 nos formatea la salida del texto.
            except TypeError as e:
                logging.exception('[outputUtilities.get_json_output] TypeError: ' + str(e))
            except Exception as exception:
                print('[+] Error: {}'.format(exception))
                logging.exception('[outputUtilities.get_json_output] Error with json files: {}'.format(exception))

    @classmethod
    def get_csv_output(cls, file_name, dataset_directory, item):
        """
        Generate a cvs file from user information instance. If the file exists, append info in new row.
        :return: a new csv file or a new row.
        """
        path_file = dataset_directory + '/' + file_name
        with open(file=path_file, mode='a+') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(item)

