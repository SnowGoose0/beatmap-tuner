import sys
import bm_read
import bm_audio
import bm_parse

def main():
    bm_modification_settings = bm_parse.ModifierSettings()

    for arg in sys.argv:
        arg_v = arg.split('=')

        if len(arg_v) < 2:
            continue

        arg_name = arg_v[0]
        arg_value = float(arg_v[1])
        
        if arg_name == "bpm":
            bm_modification_settings.bpm = arg_value 

        elif arg_name == "hp":
            bm_modification_settings.hp_drain = arg_value 

        elif arg_name == "cs":
            bm_modification_settings.circle_size = arg_value

        elif arg_name == "od":
            bm_modification_settings.overall_difficulty = arg_value

        elif arg_name == "ar":
            bm_modification_settings.approach_rate = arg_value

        elif arg_name == "sm":
            bm_modification_settings.slider_multiplier = arg_value

        elif arg_name == "str":
            bm_modification_settings.slider_tick_rate = arg_value


        

    rate = 1.189
    path = '/media/jason/6CACEABAACEA7E48/Users/Jason/AppData/Local/osu!/Songs/701549 Sagara Kokoro - Hoshizora no Ima/Sagara Kokoro - Hoshizora no Ima (Kyuukai) [Shooting Star].osu'
    path2 = '/media/jason/6CACEABAACEA7E48/Users/Jason/AppData/Local/osu!/Songs/553906 BLANKFIELD - Goodbye/BLANKFIELD - Goodbye (Kyubey) [Intense].osu'
    path3 = '/media/jason/6CACEABAACEA7E48/Users/Jason/AppData/Local/osu!/Songs/744772 toby fox - Last Goodbye/toby fox - Last Goodbye (Fatfan Kolek) [Extra].osu'
    path4 = "/media/jason/6CACEABAACEA7E48/Users/Jason/AppData/Local/osu!/Songs/935549 HAG - Chikyuu Saigo no Kokuhaku o (1)/HAG - Chikyuu Saigo no Kokuhaku o (iljaaz) [Kowari x Tomadoi's Insane].osu"
    # audio_path = './hoshizora-no-ima.mp3'
    # buff = bm_read.read_to_buffer(path)
    # bm_read.read_section(buff, '[General]')
    # bm_audio.bm_audio_speed(audio_path, rate)

    BM = bm_parse.Beatmap(path4)
    BM.parse()
    BM.apply(bm_modification_settings)


main()