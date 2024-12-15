from system.modules.module import Module
import json
import yaml
import sys
import xml.etree.ElementTree as ET
import xmltodict
import csv
from typing import Dict

class Text(Module):
    def __init__(self):
        supportedFormats = (
            "txt","json","yaml","yml","xml","csv"
        )
        super().__init__(supportedFormats)

    def convert(self, filepath: str, output: str):
        fromFormat = filepath.split(".")[-1]
        toFormat = output.split(".")[-1]
        if fromFormat == toFormat:
            print("can't convert to same type: ",fromFormat, " to ",toFormat)
            sys.exit(1)

        else:
            try:
                data: Dict = self.readFile(filepath, fromFormat)

                if type(data) != type({}):#if it isnt a dictionary
                    print("error reading file")
                    sys.exit(1)

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
                    case "txt":
                        print("Singularty cannot convert to a txt file. Please use: json, xml, yaml,...")
                        sys.exit(1)
                    case "csv":
                        print("EARY IMPLEMENTATION")#TODO:Improve csv exports
                        with open(output, 'w', newline='') as file:
                            writer = csv.DictWriter(file, fieldnames=data.keys())
                            writer.writeheader()
                            writer.writerow(data)
                    case _:
                        print("error finding format "+toFormat+". This is a bug")
                        sys.exit(1)
            except Exception as e:
                print(e)

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
                case _:
                    print("Error reading file")
                    sys.exit(1)

    def dict_to_xml(self, root_element, data):
        elem = ET.SubElement(root_element, root_element.tag)

        for key, value in data.items():
            if isinstance(value, dict):
                child_elem = ET.SubElement(elem, key)
                self.dict_to_xml(child_elem, value)
            else:
                ET.SubElement(elem, key).text = str(value)
