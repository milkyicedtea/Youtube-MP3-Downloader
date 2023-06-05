####################
#                  #
#     yt-Mp3dl     #
#                  #
####################

from downloader import Downloader

import itertools
import json
import yaml


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
								urls = open(file, 'r').readlines()
								print(f'txt urls {urls}')
								downloader.Download(urls)

							case ".json":
								json_data = json.load(open(file))
								# print(json_data)
								for value in json_data['entries']:
									urls = value['value']
									downloader.Download(urls)

							case ".yaml":
								with open(file, 'r') as yaml_file:
									yaml_data = yaml.full_load(yaml_file)
								# print(yaml_data)
								urls = list(itertools.chain(*[data for item, data in yaml_data.items()]))
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
