########################
#                      #
#     yt-Mp3dl-GUI     #
#                      #
########################

from downloader import Downloader

import PySimpleGUI as sg

import itertools
import json
import yaml


def main_app(win: sg.Window):
    downloader = Downloader()

    while True:
        event, values = win.read()

        if event in [sg.WIN_CLOSED, 'Exit_Program']:
            del downloader
            break

        if event in ['Download_Button']:
            urls = [value for index, value in values.items()]
            print(urls)
            downloader.Download(urls)
            downloader.WriteJson()
            # urls = list(itertools.chain(*values[1]))
            # print(urls)


        if event in ['File_Import']:
            file_found: bool = False
            for file in downloader.directory.iterdir():
                # print(file)
                # print(file.name)
                # if file.name[:-len(file.suffix)] in ['urls', 'urls_template']:    # easy access to use templates instead of new files
                if file.name[:-len(file.suffix)] in ["urls"]:
                    file_found = True
                    match file.suffix:
                        case ".txt":
                            urls = open(file, 'r').readlines()
                            print(f'txt urls {urls}')
                            # downloader.Download(urls)
                            # POPUP

                        case ".json":
                            json_data = json.load(open(file))
                            # print(json_data)
                            for value in json_data['entries']:
                                urls = value['value']
                                # downloader.Download(urls)
                                # POPUP

                        case ".yaml":
                            with open(file, 'r') as yaml_file:
                                yaml_data = yaml.full_load(yaml_file)
                            # print(yaml_data)
                            urls = list(itertools.chain(*[data for item, data in yaml_data.items()]))
                            # downloader.Download(urls)
                            # POPUP

                    downloader.WriteJson()
            if not file_found:
                print('You have no file named urls.* in your folder.'
                      '\nPlease make sure that the file is in the same folder as the program')

            break

    win.close()



if __name__ == "__main__":
    layout = [
        [sg.Text('YT-Mp3dl', font = '_ 15', justification = 'c', expand_x = True)],
        [sg.Text('Insert the link(s) to download here or import them from a file')],
        [sg.InputText(default_text = '', size = 45)],
        [sg.Button(button_text = 'Download', key = 'Download_Button'),
            sg.Button(button_text = 'Import from file', key = 'File_Import')],
        [sg.Button(button_text = 'Exit', key = 'Exit_Program')]
    ]
    window = sg.Window('YT-Mp3dl', layout,  resizable = True, grab_anywhere_using_control = True, finalize = False)
    main_app(window)