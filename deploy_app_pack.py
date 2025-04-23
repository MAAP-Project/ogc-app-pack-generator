'''
Deploy application package
'''
import yaml
import requests
import argparse
import os
import json

def deploy_app_pack(template_file, process_cwl_url, app_pack_registry):
    with open(template_file, 'r') as f:
        data = yaml.safe_load(f)

    if data.get("executionUnit", {}).get("href"):
        data["executionUnit"]["href"] = process_cwl_url

    maap_pgt_token = os.getenv('MAAP_PGT')
    if not maap_pgt_token:
        print("Environment variable `MAAP_PGT` is not set.")
        exit(1)

    headers = {
        'proxy-ticket': maap_pgt_token
    }

    r = requests.post(app_pack_registry, data=json.dumps(data), headers=headers)
    print(r)
    r.raise_for_status()
    print(r.text)
    print("Application package successfully deployed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy application package.")
    parser.add_argument("--process-cwl-url", type=str, help="URL to process CWL describing application package to deploy", required=True)
    parser.add_argument("--registry", type=str, help="Application package registry to deploy application package to.")
    parser.add_argument("--app-pack-template-file", type=str, default="ogc_app_pack/templates/ogcapppkg.yml", help="Path to the OGC API processes compliant OGC application package schema template.")

    args = parser.parse_args()

    deploy_app_pack(process_cwl_url=args.process_cwl_url, app_pack_registry=args.registry, template_file=args.app_pack_template_file)