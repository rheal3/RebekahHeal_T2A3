import json

class File:

    @classmethod
    def save_to_file(cls, file_path, data):
        with open(file_path, 'w') as save_file:
            json_data = json.dumps(data)
            save_file.write(json_data)
        print("Data Saved.")

    @classmethod
    def load_data(cls, file_path):
        try:
            with open(file_path, 'r') as save_file:
                json_data = json.loads(save_file.read())
                return json_data
        except:
            return {}
