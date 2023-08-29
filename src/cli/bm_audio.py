from pydub import AudioSegment
from pydub.utils import mediainfo

def bm_audio_speed(audio_file_path: str, rate: float):
    audio_base = AudioSegment.from_file(audio_file_path)
    bitrate_base = mediainfo(audio_file_path)['bit_rate']
    audio_adjusted_rate = audio_base.speedup(rate, 150, 25)
    audio_adjusted_rate.export("changed.mp3", format="mp3", bitrate=bitrate_base)