import json


class Utils:

    @classmethod
    def json_to_string(json_information):
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
