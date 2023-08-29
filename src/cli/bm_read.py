def read_to_buffer(bm_file_path: str):
    with open(bm_file_path, 'r') as bm_file_descriptor:
        return bm_file_descriptor.read()

def read_section(bm_buffer: str, section_name: str):
    if section_name[0] != '[' and section_name[-1] != ']':
        return None
    
    bm_buffer_parsed = bm_buffer.split('\n')
    section_pointer_front = bm_buffer_parsed.index(section_name)
    section_pointer_back = section_pointer_front

    while bm_buffer_parsed[section_pointer_back] != '':
        section_pointer_back += 1

    section = bm_buffer_parsed[section_pointer_front : section_pointer_back]

    return section
    
