import os
import multiprocessing
import random
import soundfile as sf
import pyrubberband as pyrb
from pydub import AudioSegment
from pydub.utils import mediainfo

class BeatmapSong():
    def __init__(self, song_path: str):
        self.__audio_path = song_path.strip()
        self.__audio_format = os.path.splitext(song_path)[1]
        self.__audio_id_hash = random.getrandbits(128)
        self.__tmp_audio_path = ''
        self.__load_audio_file()
    
    def __load_audio_file(self):
        audio_segment = None

        if self.__audio_format == '.mp3':
            audio_segment = AudioSegment.from_mp3(self.__audio_path)
        elif self.__audio_format == '.ogg':
            audio_segment = AudioSegment.from_ogg(self.__audio_path)
        elif self.__audio_format == '.wav':
            pass
        else:
            return None
        
        current_dir = os.path.dirname(os.path.realpath(__file__))

        if not os.path.isdir(os.path.join(current_dir, 'tmp')):
            os.mkdir(os.path.join(current_dir, 'tmp'))
        
        if self.__audio_format != '.wav':
            tmp_file_name = '.'.join([str(self.__audio_id_hash), 'wav'])
            self.__tmp_audio_path = os.path.join(current_dir, 'tmp', tmp_file_name)

            audio_segment.export(self.__tmp_audio_path, format='wav')

    def __speed_up(self, rate: float):
        sound_data, sample_rate = sf.read(self.__tmp_audio_path)

        sped_sound_data = pyrb.time_stretch(sound_data, sample_rate, rate)
        sf.write("test.wav", sped_sound_data, sample_rate, format='wav')

        os.remove(self.__tmp_audio_path)
        self.__tmp_audio_path = ''

    def speed_up(self, rate: float):
        speed_proc = multiprocessing.Process(target=self.__speed_up(rate))
        speed_proc.start()
        speed_proc.join()    