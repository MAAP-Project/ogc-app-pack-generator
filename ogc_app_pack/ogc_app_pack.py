'''
Generates the process.cwl
'''

import os
# Use ruamel to output just list with block style and not dicts to preserve formatting as in the template
from ruamel.yaml import YAML
import logging
import sys
import json

logger = logging.getLogger()

LOCAL_PATH = os.path.dirname(os.path.realpath(__file__))
yaml = YAML(typ='rt')

class AppPackGenerator:

    def __init__(self):
        templatedir = os.path.join(LOCAL_PATH, 'templates')
        self.process_cwl = self._load_template(os.path.join(templatedir, 'process.cwl'))

    def _load_template(self, process_cwl_fname):
        try:
            with open(process_cwl_fname, 'r') as f:
                return yaml.load(f)
        except Exception as e:
            logging.error("An error occurred: %s", str(e))

    def generate_process_cwl(self, data):
        # data = json.loads(data)

        # Handle overview info
        self.process_cwl['$graph'][0]['label'] = data['algorithm_name']
        self.process_cwl['$graph'][0]['id'] = data['algorithm_name']
        self.process_cwl['$graph'][0]['doc'] = data['algorithm_description']
        self.process_cwl['s:softwareVersion'] = data['algorithm_version']

        # Handle inputs
        count = 1
        tmp_input_defs = {}
        tmp_input_mapping = {}
        tmp_input_binding = {}
        for i in data['inputs']:
            print(i)
            tmp_input_mapping[i['name']] = i['name']
            tmp_input_defs[i['name']] = {'type': i.get("type", "string"), 'label': i['name'], 'doc': i.get("doc", ""),
                                         'default': i.get("default", "")}
            input_binding = {'position': count}
            if i.get("prefix"):
                input_binding.update({"prefix": i.get("prefix")})
            tmp_input_binding[i['name']] = {'type': i.get("type", "string"), 'inputBinding': input_binding}
            count += 1

        self.process_cwl['$graph'][0]['inputs'] = tmp_input_defs
        self.process_cwl['$graph'][0]['steps']['process']['in'] = tmp_input_mapping
        self.process_cwl['$graph'][1]['inputs'] = tmp_input_binding

        # Handle outputs
        workflow_output_definition = {}
        tmp_output_mapping = {}
        tmp_output_binding = {}

        if 'outputs' in data:
            for i in data['outputs']:
                tmp_input_mapping[i['name']] = i['name']
                workflow_output_definition[i['name']] = {'type': i['type'], 'label': i['name'], 'doc': '', 'default': ''}
                tmp_output_binding[i['name']] = {'type': i['type'], 'outputBinding': i['outputBinding']}

        # self.process_cwl['$graph'][0]['outputs'] = workflow_output_definition
        # self.process_cwl['$graph'][0]['steps']['process']['out'] = tmp_output_mapping
        # self.process_cwl['$graph'][1]['outputs'] = tmp_output_binding

        # Handle remaining fields
        self.process_cwl['$graph'][1]['requirements']['DockerRequirement']['dockerPull'] = data['docker_container_url']
        self.process_cwl['$graph'][1]['baseCommand'] = f"/app/{data['run_command']}"

        # Write process.cwl data to file
        output_file_name = f"process_cwl/{data['algorithm_name']}.{data['algorithm_version']}.process.cwl"
        with open(output_file_name, 'w', encoding='utf-8') as f:
            yaml.dump(self.process_cwl, f)
        with open("process.cwl", 'w', encoding='utf-8') as f:
            yaml.dump(self.process_cwl, f)


