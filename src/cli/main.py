import random
import beatmap
from osz import *
from utils.colors import *
from utils.log import *

def main_process():
    osz_path = prompt('enter the path to the osz file')
    osz_path = './hoshizora.osz'

    osz = BeatMapOsz('./hoshizora.osz')
    beatmap_difficulties = osz.difficulties

    for i in range(len(beatmap_difficulties)):
        log(f'[{i + 1}]: {beatmap_difficulties[i]}', TermColors.OKGREEN, True)

    difficulty_index = prompt(f'select the difficulty (1-{len(beatmap_difficulties)})')
    selected_difficulty = beatmap_difficulties[difficulty_index - 1]

    print(f'you chose: {selected_difficulty}')

    argv = prompt('enter (space separated) mod options for the beatmap (format: opt=val)\noptions available: bpm (or rate), ar, od, cs, hp')

    if argv == None:
        return 0

    bm_modification_settings = beatmap.ModifierSettings()

    argv = argv.split(' ')
    for arg in argv:
        arg_v = arg.split('=')

        if len(arg_v) < 2:
            continue

        arg_name = arg_v[0]
        arg_value = float(arg_v[1])
        
        if arg_name == "bpm":
            bm_modification_settings.bpm = arg_value 

        elif arg_name == "rate":
            bm_modification_settings.rate = arg_value

        elif arg_name == "hp":
            bm_modification_settings.hp_drain = arg_value 

        elif arg_name == "cs":
            bm_modification_settings.circle_size = arg_value

        elif arg_name == "od":
            bm_modification_settings.overall_difficulty = arg_value

        elif arg_name == "ar":
            bm_modification_settings.approach_rate = arg_value

    argument_validation = bm_modification_settings.validate_settings()

    if (not argument_validation[0]):
        log(argument_validation[1], TermColors.FAIL, True)
        return 1

    bm = beatmap.BeatmapBuilder(osz_path, selected_difficulty)
    bm.parse()

    difficulty_file_name = bm.modify(bm_modification_settings)
    difficulty_content = bm.serialize()

    with open('.'.join([difficulty_file_name, 'osu']), 'w') as f:
        f.write(difficulty_content)

    return 0

def main():
    while(1):
        if main_process() > 0:
            exit(0)

if __name__ == '__main__':
    main()