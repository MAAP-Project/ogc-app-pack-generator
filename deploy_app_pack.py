'''
Deploy application package
'''
import yaml
import requests
import argparse
import os
import json


def submit_request(url, data, headers):
    """
    Submit a request to the application package registry. A POST request is attempted first. If the response to the POST
    is an HTTP status code of 409, this indicates the process already exists then a PUT request will be submitted,
    overwriting the existing process.

    Args:
        url (str): The registry URL.
        data (dict): The request body, containing the process CWL URL or path.
        headers (dict): The request headers.

    Returns:
        dict or Exception: 
            - On success, returns the JSON response from the server.
            - On HTTPError (status code 409), attempts to submit a PUT request and returns the JSON response.
            - On other errors, returns the exception raised during the request process.

    Raises:
        RequestException: If the HTTP response status code is greater than 400.
        Exception: For all other exceptions.
    """
    try:
        r = requests.post(url, data=json.dumps(data), headers=headers)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 409:
            print("Process exists. Overwriting existing process.")
            r = requests.put(url, data=json.dumps(data), headers=headers)
            r.raise_for_status()
            return r.json()
        else:
            return e
    except Exception as e:
        return e


def deploy_app_pack(process_cwl_url, app_pack_registry, template_file):
    """
    Builds a request to deploy an application package process CWL to a specified registry.

    Args:
        process_cwl_url (str): The URL or path to the process CWL.
        app_pack_registry (str): The URL of the application package registry to which the process will be deployed.
        template_file (str): The path to the YAML template file containing the deployment request.

    Returns:
        None
        
    Raises:
        ValueError: Raises a ValueError if the MAAP_PGT token is not set. This token is required to deploy processes.
    """
    with open(template_file, 'r') as f:
        data = yaml.safe_load(f)

    if data.get("executionUnit", {}).get("href"):
        data["executionUnit"]["href"] = process_cwl_url

    maap_pgt_token = os.getenv('MAAP_PGT')
    if not maap_pgt_token:
        raise ValueError("Environment variable `MAAP_PGT` is not set.")

    headers = {
        'proxy-ticket': maap_pgt_token,
        'Content-Type': 'application/json'
    }

    r = submit_request(app_pack_registry, data, headers)
    print(r)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy application package.")
    parser.add_argument("--process-cwl-url", type=str, help="URL or path to process CWL describing application package to deploy", required=True)
    parser.add_argument("--registry", type=str, help="Application package registry to deploy application package to.")
    parser.add_argument("--app-pack-template-file", type=str, default="templates/ogcapppkg.yml", help="Path to the OGC API processes compliant OGC application package schema template.")

    args = parser.parse_args()
    print(f"Parameters: \n \
    Process CWL: {args.process_cwl_url} \n \
    Application package registry: {args.registry} \n \
    Template file: {args.app_pack_template_file}")

    with open(args.app_pack_template_file, 'r') as f:
        data = yaml.safe_load(f)
        
    deploy_app_pack(process_cwl_url=args.process_cwl_url, app_pack_registry=args.registry, template_file=args.app_pack_template_file)
