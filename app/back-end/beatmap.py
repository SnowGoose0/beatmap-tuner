import os
from song import BeatmapSong
from collections import defaultdict
from zipfile import ZipFile

class ModifierSettings:
    def __init__(self, settings={}):
        init = None

        if settings == {}:
            self.hp_drain = init
            self.circle_size = init
            self.overall_difficulty = init
            self.approach_rate = init
            self.bpm = init
            self.rate = init

        else:
            self.hp_drain = float(settings['hp'])
            self.circle_size = float(settings['cs'])
            self.overall_difficulty = float(settings['od'])
            self.approach_rate = float(settings['ar'])
            self.bpm = float(settings['bpm'])
            self.rate = float(settings['rate'])

    def validate_settings(self):
        setting_fields = vars(self)

        if self.bpm != None and self.rate != None:
            return (False, "ARGUMENT ERROR: song speed ambiguity - rate and bpm cannot both be used at once")

        for setting, value in setting_fields.items():
            if value == None:
                continue

            match setting:
                case 'bpm':
                    if value <= 0:
                        return (False, 'ARGUMENT ERROR: bpm must be > 0')
                
                case 'rate':
                    if value > 2 or value < 1:
                        return (False, 'ARGUMENT ERROR: rate must be between 1 and 2')
                    
                case 'hp_drain':
                    if value > 10 or value < 0:
                        return (False, 'ARGUMENT ERROR: HP drain must be between 0 and 10')
                    
                case 'circle_size':
                    if value > 10 or value < 0:
                        return (False, 'ARGUMENT ERROR: CS must be between 0 and 10')
                    
                case 'overall_difficulty':
                    if value > 10 or value < 0:
                        return (False, 'ARGUMENT ERROR: OD must be between 0 and 10')
                    
                case 'approach_rate':
                    if value > 10 or value < 0:
                        return (False, 'ARGUMENT ERROR: AR must be between 0 and 10')

        return (True, 'SUCCESS')

class BeatmapBuilder:
    BEATMAP_VERSION_IDENTIFIER = 'osu file format v14'
    BEATMAP_PAIRED_SECTIONS = ['General', 'Editor', 'Metadata', 'Difficulty', 'Colours']
    BEATMAP_COMMA_SECTIONS = ['Events', 'TimingPoints', 'HitObjects']
    BEATMAP_SECTIONS_LABELS = ['General', 'Editor', 'Metadata', 'Difficulty', 'Events', 'TimingPoints', 'Colours', 'HitObjects']

    BEATMAP_TAG_NAME = 'osubma'

    MINUTE_MS = 60000

    def __init__(self, file_path: str, difficulty_name: str):        
        self.__bm_osz_file_path = file_path
        self.__bm_difficulty = difficulty_name
        self.__bm_buffer = self.__split_buffer_sections()
        self.__bm_sections = {}
        
    def parse(self):
        for section in self.__bm_buffer:
            section_semi_parsed = self.__format_section(section)
            
            if section_semi_parsed != None:
                self.__bm_sections.update(section_semi_parsed)

        for section in self.__bm_sections.keys():
            section_delimiter = ','

            if section in self.BEATMAP_PAIRED_SECTIONS:
                section_delimiter = ':'

            for line_index in range(len(self.__bm_sections[section])):
                line_content = self.__bm_sections[section][line_index]
                self.__bm_sections[section][line_index] = line_content.strip().split(section_delimiter)

    def get_default_settings(self):
        difficulty_settings = self.__bm_sections['Difficulty']

        return {
            'hp': int(difficulty_settings[0][1]),
            'cs': float(difficulty_settings[1][1]),
            'od': float(difficulty_settings[2][1]),
            'ar': round(float(difficulty_settings[3][1]), 2),
            'rate': 1.00,
            'bpm': self.__persistent_bpm(),
        }
    
    def modify(self, settings: ModifierSettings):
        general_settings = self.__bm_sections['General']
        time_point_settings = self.__bm_sections['TimingPoints']
        metadata_settings = self.__bm_sections['Metadata']
        difficulty_settings = self.__bm_sections['Difficulty']

        modified_rate = settings.rate

        if settings.bpm != None:
            modified_rate = settings.bpm / self.__persistent_bpm()

        modified_rate = round(modified_rate, 3)

        if modified_rate != None:
            for tp_index in range(len(self.__bm_sections['TimingPoints'])):
                time_point = time_point_settings[tp_index]

                if len(time_point) < 8:
                    continue

                time_point[0] = str(int(float(time_point[0]) // modified_rate))

                if int(time_point[6]) == 1:
                    time_point[1] = str(float(time_point[1]) / modified_rate)

            for hit_object_index in range(len(self.__bm_sections['HitObjects'])):
                hit_object = self.__bm_sections['HitObjects'][hit_object_index]

                if len(hit_object) < 5:
                    continue

                hit_object[2] = str(int(float(hit_object[2]) // modified_rate))

            general_settings[2][1] = str(int(int(general_settings[2][1]) // modified_rate))

            metadata_settings[5][1] += f' x{modified_rate}'
        
        if settings.hp_drain != None:
            difficulty_settings[0][1] = str(int(settings.hp_drain))
            metadata_settings[5][1] += f' HP{settings.hp_drain}'

        if settings.circle_size != None:
            difficulty_settings[1][1] = str(settings.circle_size)
            metadata_settings[5][1] += f' CS{settings.circle_size}'

        if settings.overall_difficulty != None:
            difficulty_settings[2][1] = str(settings.overall_difficulty)
            metadata_settings[5][1] += f' OD{settings.overall_difficulty}'

        if settings.approach_rate != None:
            difficulty_settings[3][1] = str(settings.approach_rate)
            metadata_settings[5][1] += f' AR{settings.approach_rate}'

        metadata_settings[5] += f' - {self.BEATMAP_TAG_NAME} {modified_rate}'
        metadata_settings[7] += self.BEATMAP_TAG_NAME

        if modified_rate > 1:
            audio_file_name = general_settings[0][1].strip()
            self.__extract_osz_audio(audio_file_name)

            audio_export_name = f'{os.path.splitext(audio_file_name)[0]} - x{modified_rate}'
            audio_export_path = os.path.dirname(self.__bm_osz_file_path)

            song = BeatmapSong(audio_file_name, audio_export_path, audio_export_name)
            song.speed_up(modified_rate)

            audio_file_name = general_settings[0][1] = ' ' + audio_export_name + '.wav'

        artist = metadata_settings[2][1]
        title = metadata_settings[0][1]
        creator = metadata_settings[4][1]
        version = metadata_settings[5][1]

        return f'{artist} - {title} ({creator}) [{version}]'
        

    def serialize(self):
        if self.__bm_sections == {}:
            print('SERIALIZATION ERROR: nothing was parsed - nothing to serialize')
            return
        
        beatmap_serialized = []

        for section_label in self.BEATMAP_SECTIONS_LABELS:
            section_serialized = section_label + '\n'
            section_serialized = f'[{section_label}]\n'
            section_format_paired = False

            if section_label in self.BEATMAP_PAIRED_SECTIONS:
                section_format_paired = True

            for section_line in self.__bm_sections[section_label]:
                if len(section_line) == 1 and section_line[0] == '':
                    section_serialized += '\n'
                    continue

                if section_format_paired:
                    key = section_line[0]
                    value = ':'.join(section_line[1:])

                    section_serialized += (f'{key}:{value}')

                else:
                    section_serialized += ','.join(section_line)

                section_serialized += '\n'
            
            beatmap_serialized.append(section_serialized)
        
        return 'osu file format v14\n\n' + ''.join(beatmap_serialized)

    def __extract_osz_audio(self, audio_file_name: str):    
        zip_path = self.__bm_osz_file_path
        
        with ZipFile(zip_path, mode='r') as osz_archive:
            return osz_archive.extract(audio_file_name)       
    
    def __read_osz_to_buffer(self): 
        zip_path = self.__bm_osz_file_path
        difficulty_name = self.__bm_difficulty
        
        with ZipFile(zip_path, mode='r') as osz_archive:
            target_path = '.'.join([difficulty_name, 'osu'])
            return osz_archive.read(target_path).decode(encoding='utf-8')
        
    def __format_section(self, bm_section_buffer: str):
        bm_section_line_buffer = bm_section_buffer.split('\n')[:-1]
        bm_section_id = bm_section_line_buffer[0]

        if bm_section_id[0] != '[' and bm_section_id[-1] != ']':
            return
        
        bm_section_entry = {
            bm_section_id.strip()[1:-1] : bm_section_line_buffer[1:]
        }
        
        return bm_section_entry
    
    def __split_buffer_sections(self):
        buffer = self.__read_osz_to_buffer()
        section_buffer = []

        section_frame_front = 0
        buffer_cursor = 0

        while (buffer_cursor != len(buffer)):

            if buffer[buffer_cursor] == '[':
                label_cursor = buffer_cursor

                while label_cursor < len(buffer) and buffer[label_cursor] != ']':
                    label_cursor += 1

                section_label = buffer[buffer_cursor + 1 : label_cursor]
                
                if section_label.strip() in self.BEATMAP_SECTIONS_LABELS:
                    section_buffer.append(buffer[section_frame_front : buffer_cursor])
                    
                    section_frame_front = buffer_cursor
                
            buffer_cursor += 1

        section_buffer.append(buffer[section_frame_front:])

        return section_buffer
    
    def __persistent_bpm(self):
        tp_duration = defaultdict(int)
        current_bl = 0
        current_bl_time = 0
        max_time = 0
        
        for tp in self.__bm_sections['TimingPoints']:
            if len(tp) < 8:
                continue

            if float(tp[6]) == 0:
                max_time = float(tp[0])
                continue
            
            bl_duration = float(tp[0]) - current_bl_time
            tp_duration[current_bl] += bl_duration

            current_bl = float(tp[1])
            current_bl_time = float(tp[0])


        bl_duration = max_time - current_bl_time
        tp_duration[current_bl] += bl_duration

        bl_max = max(tp_duration, key=lambda k: tp_duration[k])

        return self.MINUTE_MS /  bl_max