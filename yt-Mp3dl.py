####################
#                  #
#     yt-Mp3dl     #
#                  #
####################

from downloader import Downloader

from cases import Cases


def Selection():
    while True:
        selection = input("Select how to input you link(s)."
                          "\nPress 1 to read from file or 2 to input manually. ")
        match selection:
            case "1":
                file_found: bool = False
                for file in downloader.directory.iterdir():
                    # print(file)
                    # print(file.name)
                    # if file.name[:-len(file.suffix)] in ['urls', 'urls_template']:    # easy access to use templates instead of new files
                    if file.name[:-len(file.suffix)] in ["urls"]:
                        file_found = True
                        match file.suffix:
                            case ".txt":
                                urls = Cases.caseTxt(file)
                                # print(f'txt urls {urls}')
                                downloader.Download(urls)

                            case ".json":
                                urls = Cases.caseJson(file)
                                downloader.Download(urls)

                            case ".yaml":
                                urls = Cases.caseYaml(file)
                                downloader.Download(urls)

                        downloader.WriteJson()
                if not file_found:
                    print('You have no file named urls.* in your folder.'
                          '\nPlease make sure that the file is in the same folder as the program')

                break

            case "2":
                urls: list = [input("Input the link you want to want to download from. ")]
                downloader.Download(urls)
                downloader.WriteJson()
                break

            case _:  # case _ = case other
                print("Invalid input: try re-entering you selection.")


if __name__ == "__main__":
    downloader = Downloader()
    Selection()
