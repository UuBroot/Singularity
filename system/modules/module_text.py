from system.modules.module import Module
import json
import yaml
import xml.etree.ElementTree as ET
import xmltodict
import csv
from typing import Dict

from global_vars import globals, FinishedType

class Text(Module):
    def __init__(self):
        supportedFormats = (
            "json","yaml","yml","xml","csv"
        )
        super().__init__(supportedFormats)

    def checkDependencies(self)-> bool:
        return True

    def convert(self, filepath: str, output: str):
        fromFormat = filepath.split(".")[-1]
        toFormat = output.split(".")[-1]

        try:
            data: Dict = self.readFile(filepath, fromFormat)
            
            if type(data) != type({}):#if it isnt a dictionary
                print("error reading file")
                return
            match toFormat:
                case "yaml":
                    with open(output, 'w') as file:
                        yaml.dump(data, file)
                case "yml":
                    with open(output, 'w') as file:
                        yaml.dump(data, file)
                case "json":
                    with open(output, 'w') as file:
                        json.dump(data, file)
                case "xml":
                    root =  ET.Element('root')
                    self.dict_to_xml(root, data)

                    xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
                    xml_str += ET.tostring(root, encoding='unicode')

                    with open(output, 'w') as file:
                        file.write(xml_str)
                case "csv":
                    print("EARY IMPLEMENTATION")#TODO:Improve csv exports                        
                    with open(output, 'w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=data.keys())
                        writer.writeheader()
                        writer.writerow(data)
                case _:
                    print("error finding format "+toFormat+". This is a bug")
                    return
        except Exception as e:
            print(e)
            globals.update(finishedType=FinishedType.FILECORRUPT)
            return
                
        globals.update(finishedType=FinishedType.FINISHED)

    def readFile(self, path, format)-> Dict:
        with open(path, 'r') as file:
            match format:
                case "json":
                    return json.load(file)
                case "yaml":
                    return yaml.safe_load(file)
                case "yml":
                    return yaml.safe_load(file)
                case "xml":
                    return xmltodict.parse(str(file.read()))
                case "csv":
                    reader = csv.DictReader(file)
                    dict = {}
                    for row in reader:
                        for key, value in row.items():
                            if key in dict:
                                if not isinstance(dict[key], list):
                                    dict[key] = [dict[key]]
                                dict[key].append(value)
                            else:
                                dict[key] = value
                    return dict
                case _:
                    globals.update(finishedType=FinishedType.FILENOTSUPPORTED)
                    return

    def dict_to_xml(self, root_element, data):
        elem = ET.SubElement(root_element, root_element.tag)

        for key, value in data.items():
            if isinstance(value, dict):
                child_elem = ET.SubElement(elem, key)
                self.dict_to_xml(child_elem, value)
            else:
                ET.SubElement(elem, key).text = str(value)
