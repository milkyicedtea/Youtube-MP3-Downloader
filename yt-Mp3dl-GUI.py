########################
#                      #
#     yt-Mp3dl-GUI     #
#                      #
########################

from downloader import Downloader
from cases import Cases

from pathlib import Path

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
                # if file.name[:-len(file.suffix)] in ['urls', 'urls_template']:    # easy switch between templates and new files
                if file.name[:-len(file.suffix)] in ["urls"]:
                    file_found = True
                    match file.suffix:
                        case ".txt":
                            urls = Cases.caseTxt(file)
                            print(f'txt urls {urls}')
                            # downloader.Download(urls)

                        case ".json":
                            urls = Cases.caseJson(file)
                            # downloader.Download(urls)
                            # POPUP

                        case ".yaml":
                            urls = Cases.caseYaml(file)
                            # downloader.Download(urls)
                            # POPUP

                    downloader.WriteJson()
            if not file_found:
                file = sg.popup_get_file('You have no file(s) named urls.* in your folder.'
                                         "\nPlease select a file or make sure that it is in the program's folder")
                if file:
                    match Path(file).suffix:
                        case ".txt":
                            urls = Cases.caseTxt(file)
                            # print(f'txt urls {urls}')
                            # downloader.Download(urls)

                        case ".json":
                            urls = Cases.caseJson(file)
                            # print(f'json urls {urls}')
                            # downloader.Download(urls)
                            # POPUP
                            for index, url in urls:
                                if index < len(urls):
                                    stringifiedlist: str = stringifiedlist + url + ", "
                                else:
                                    stringifiedlist += url
                            sg.popup_ok_cancel(f'Found these links:'
                                               f' {[url for url in urls]}')

                        case ".yaml":
                            urls = Cases.caseYaml(file)
                            # print(f'yaml urls {urls}')
                            # downloader.Download(urls)
                            # POPUP

                # print('You have no file named urls.* in your folder.'
                #       '\nPlease make sure that the file is in the same folder as the program')

    win.close()


if __name__ == "__main__":
    layout = [
        [sg.Text('YT-Mp3dl', font='_ 15', justification='c', expand_x=True)],
        [sg.Text('Insert the link(s) to download here or import them from a file')],
        [sg.InputText(default_text='', size=45)],
        [sg.Button(button_text='Download', key='Download_Button'),
         sg.Button(button_text='Import from file', key='File_Import')],
        [sg.Button(button_text='Exit', key='Exit_Program')]
    ]
    window = sg.Window('YT-Mp3dl', layout, resizable=True, grab_anywhere_using_control=True, finalize=False)
    main_app(window)
