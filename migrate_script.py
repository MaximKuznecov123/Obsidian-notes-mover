"""README
1) place all notes for import in one folder and root note too(it will be your old_vault)
2) change key parameters
3) enjoy
"""


"""
It works for me but maybe you'll have following problems:

1) Infinite loop if file links to self or backlinked file
2) Quotes issues
3) All logs are red

I will refine this code as I can and update message on forum
"""
import re
import os

attachments_extensions = ('.jpg', '.jpeg', '.jpe', '.jif', '.png', '.gif', '.svg', '.svgz', '.pdf', '.raw', '.arw',)

# key parameters
# DO NOT REPLACE DOUBLE BACKSLASHES ON THE END
old_vault = 'path\\to\\your\\OLD_VAULT\\'
new_vault = 'path\\to\\your\\NEW_VAULT\\'

attachments_old_directory = 'path\\to\\your\\ATTACHMENTS_OLD_DIR\\'
attachments_new_directory = 'path\\to\\your\\ATTACHMENTS_NEW_DIR\\'
root_file = 'YOUR_ROOT_NOTE.md'


def my_cut(str_: str) -> str:
    index = str_.find('|')
    return str_[2: index if index != -1 else -2]


def fun(file_relative: str, place: str, destination: str, attachments_dir: str, attachments_dest: str):
    with open(place + file_relative, 'r', encoding='utf-8') as file:
        content = file.read()
        raw_files = list(map(my_cut, re.findall('\[\[.*]]', content)))

        notes, attachments = [], []
        for each in raw_files:
            (attachments if [ext for ext in attachments_extensions if each.endswith(ext)] else notes).append(each)
        notes = list(map(lambda x: x + '.md', notes))

        print('Outgoing notes:', notes)
        print('Attachments:', attachments)

        for each in notes:
            print(each)
            try:
                fun(each, place, destination, attachments_dir, attachments_dest)
            except FileNotFoundError:
                print(f'\033[91m {file_relative} probably already replaced so we do nothing ¯\\_(ツ)_/¯\033[0m')

        for each in attachments:
            print(each)
            try:
                os.replace(attachments_dir + each, attachments_dest + each)
                print(f'{each} MOVED!')
            except FileNotFoundError:
                print(f'\033[91m{each} probably already replaced so we do nothing ¯\\_(ツ)_/¯\033[0m')

    os.replace(place + file_relative, destination + file_relative)
    print(f'{file_relative} MOVED!')


fun(root_file, old_vault, new_vault, attachments_old_directory, attachments_new_directory)
# sorry for bad english
