import json
import yaml
import itertools


class Cases:

    @staticmethod
    def caseTxt(file):
        urls = open(file, 'r').readlines()
        return urls

    @staticmethod
    def caseJson(file):
        urls: list = []
        json_data = json.load(open(file))
        # print(json_data)
        for value in json_data['entries']:
            urls.append(value['value'])
        return urls

    @staticmethod
    def caseYaml(file):
        with open(file, 'r') as yaml_file:
            yaml_data = yaml.full_load(yaml_file)
        # print(yaml_data)
        urls = list(itertools.chain(*[data for item, data in yaml_data.items()]))
        return urls
