import sys
from utils.colors import TermColors

__PROMPT_PREFIX = '> '

def prompt(prompt_instruction: str):
    log(prompt_instruction, TermColors.OKGREEN, True)
    log('', TermColors.ENDC, False)
    inp = input().strip()

    if '.' in inp:
        try:
            inp = round(float(inp), 2)
        except:
            pass
    else:
        try:
            inp = int(inp)
        except:
            pass
    
    if type(inp) == str:
        if len(inp) > 256:
            return 1, 'INPUT ERROR: input is too long'
        
        inp = __parse_command(inp)
    
    return inp

def log(string: str, color: str, new_line: bool):
    if string != '':
        sep = '\n'
        string_lines = [string]
        
        if '\n' in string:
            string_lines = string.split(*list(sep if string.count(sep) else []))

        for line in string_lines:
            sys.stdout.write(color + __PROMPT_PREFIX + line + '\n' + TermColors.ENDC)

    else:
        sys.stdout.write(color + __PROMPT_PREFIX + TermColors.ENDC)
    
    if new_line:
        sys.stdout.write('\n')


def __parse_command(inp: str):
    if inp.lower() in ['exit', 'quit', 'q']:
        log('\ngoodbye!', TermColors.ENDC, True)
        exit(0)

    elif inp.lower() in ['clear', 'cls']:
        sys.stdout.write(TermColors.CLEAR)
        return None

    return inp