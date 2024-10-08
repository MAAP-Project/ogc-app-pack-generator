'''

MAAP OGC Application Package Wrapper

This is a project-specific OGC wrapper that invokes the reference implementation for 
OGC application package generation.

'''
import sys
import yaml
import json
import logging
import json
import os
from ogc_app_pack import AppPackGenerator
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app_pack.log'
)

def read_algorithm_yaml_file(filepath):
    with open(filepath, 'r') as fp:
        data = yaml.safe_load(fp)
        return data


def main(args):
    data = {}
    algo_file = args.algo_yaml
    logging.info("Generating application package using: %s", algo_file)

    # TODO: determine if input is already cwl or not
    try:
        #data = yaml.safe_load(algo_file)
        # data = json.loads(json.loads(algo_file))
        data = read_algorithm_yaml_file(algo_file)
        print("Algo data:")
        print(data)

        # OGC does not support file, positional inputs the way MAAP does, so we need to flatten the inputs.
        flattened_inputs = []
        algo_config_inputs = data.get("inputs", {})
        for value in ["positional", "config", "file", "directory"]:
            if value in algo_config_inputs:
                for k in algo_config_inputs.get(value):
                    if value == "file":
                        k.update({"type": "File"})
                    elif value == "directory":
                        k.update({"type": "Directory"})
                    elif value == "config":
                        k.update({"type": "string"})
                    else:
                        k.update({"type": "string"})
                    k.update({"prefix": f"--{k.get('name')}"})
                    flattened_inputs.append(k)

        data['inputs'] = flattened_inputs
    except Exception as e:
        logging.error("An error occurred: %s", str(e))
    
    # Generate the OGC package using the reference implementation
    print("Data for ogc:")
    data.update({"docker_container_url": args.ogc_container_url})
    print(data)

    app = AppPackGenerator()
    app.generate_process_cwl(data)
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("algo_yaml", help="Path to algo yaml file")
    parser.add_argument("ogc_container_url", help="URL of built OGC container")
    args = parser.parse_args()
    print(args)
    return_code = main(args)

