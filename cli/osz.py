import os
import zipfile

class BeatMapOsz:
    def __init__(self, osz_file_path: str):
        self.__path = osz_file_path
        self.__name = os.path.basename(osz_file_path)
        self.__content = self.__parse_content(self.__path)
        self.difficulties = [os.path.splitext(diff)[0] for diff in self.__content['beatmaps']]
    
    def __parse_content(self, path: str):
        osz_content = {
            'images': [],
            'audios': [],
            'beatmaps': [],
            'misc': [],
        }

        with zipfile.ZipFile(path, 'r') as osz:
            for file_data in osz.filelist:
                file_name = file_data.filename
                file_extension = os.path.splitext(file_name)[-1]

                if file_extension in ['.jpg', '.jpeg', 'png']:
                    osz_content['images'].append(file_name)

                elif file_extension in ['.mp3', '.wav', '.ogg']:
                    osz_content['audios'].append(file_name)

                elif file_extension == '.osu':
                    osz_content['beatmaps'].append(file_name)

                else:
                    osz_content['misc'].append(file_name)

            return osz_content