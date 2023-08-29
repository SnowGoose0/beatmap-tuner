from collections import defaultdict

class ModifierSettings:
    def __init__(self):
        self.bpm = -1
        self.hp_drain = -1
        self.circle_size = -1
        self.overall_difficulty = -1
        self.approach_rate = -1
        self.slider_multiplier = -1
        self.slider_tick_rate = -1

class Beatmap:
    BEATMAP_VERSION_IDENTIFIER = "osu file format v14"
    BEATMAP_PAIRED_SECTIONS = ["General", "Editor", "Metadata", "Difficulty", "Colours"]
    BEATMAP_COMMA_SECTIONS = ["Events", "TimingPoints", "HitObjects"]
    BEATMAP_SECTIONS_LABELS = BEATMAP_PAIRED_SECTIONS + BEATMAP_COMMA_SECTIONS

    MINUTE_MS = 60000

    def __init__(self, file_path: str):        
        self.__bm_file_path = file_path
        self.__bm_buffer = self.__split_sections()
        self.__bm_sections = {}

        # for i in self.__bm_buffer:
        #     print(i)

        if self.BEATMAP_VERSION_IDENTIFIER not in self.__bm_buffer[0]:
            print("PARSING ERROR: unrecognized beatmap version - .osu file format must be version 14")
        
    def parse(self):
        for section in self.__bm_buffer:
            section_semi_parsed = self._parse_section(section)
            
            if section_semi_parsed != None:
                self.__bm_sections.update(section_semi_parsed)

        for section in self.__bm_sections.keys():
            section_delimiter = ','

            if section in self.BEATMAP_PAIRED_SECTIONS:
                section_delimiter = ':'

            for line_index in range(len(self.__bm_sections[section])):
                line_content = self.__bm_sections[section][line_index]
                self.__bm_sections[section][line_index] = line_content.strip().split(section_delimiter)

    
    def apply(self, settings: ModifierSettings):
        self.__bm_settings = settings
        rate = 1

        print(self.__bpm())

        if settings.bpm > 0:
            current_bpm = self.__bpm()

            rate = settings.bpm / current_bpm

        print(rate)

        



    def dump(self):
        print("Dumping Shit")

    def _parse_section(self, bm_section_buffer: str):
        bm_section_line_buffer = bm_section_buffer.split('\n')
        bm_section_id = bm_section_line_buffer[0]

        if bm_section_id[0] != '[' and bm_section_id[-1] != ']':
            return
        
        bm_section_entry = {
            bm_section_id[1:-1] : bm_section_line_buffer[1:]
        }
        
        return bm_section_entry
    
    def __read_to_buffer(self):
        with open(self.__bm_file_path, 'r') as bm_file_descriptor:
            return bm_file_descriptor.read()
    
    def __split_sections(self):
        buffer = self.__read_to_buffer()
        section_buffer = []

        section_frame_front = 0
        buffer_cursor = 0

        while (buffer_cursor != len(buffer)):

            if buffer[buffer_cursor] == '[':
                label_cursor = buffer_cursor

                while label_cursor < len(buffer) and buffer[label_cursor] != ']':
                    label_cursor += 1

                section_label = buffer[buffer_cursor + 1 : label_cursor]

                if section_label in self.BEATMAP_SECTIONS_LABELS:
                    section_buffer.append(buffer[section_frame_front : buffer_cursor])

                    section_frame_front = buffer_cursor
                
            buffer_cursor += 1

        section_buffer.append(buffer[section_frame_front:])

        return section_buffer
    
    def __bpm(self):
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


        