from zipfile import ZipFile

zip_path = './hoshizora.osz'

with ZipFile(zip_path, mode='r') as osz_archive:
    osz_archive.extract('Hoshizora no Ima.mp3')  