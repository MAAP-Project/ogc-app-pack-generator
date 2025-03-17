'''
Deploy application package

To deploy the application package, make a request to the /processes endpoint of an OGC API processes compliant API.
This means making a request to the MAAP API /processes endpoint.

Pass url and creds through from action to this script

Take a look here for request details:
https://github.com/MAAP-Project/joint-open-api-specs/
https://github.com/MAAP-Project/joint-open-api-specs/blob/main/ogc-api-processes/openapi-template/schemas/processes-dru/ogcapppkg.yaml
https://github.com/MAAP-Project/joint-open-api-specs/blob/main/ogc-api-processes/openapi-template/schemas/processes-core/process.yaml

post:
  summary: deploy a process.
  description: |
    Deploys a process.

    For more information, see [Section 6.3](http://docs.ogc.org/DRAFTS/20-044.html#_87a6983e-d060-458c-95ab-27e232e64822).
  operationId: deploy
  tags:
    - DRU
  requestBody:
    description: |-
      An OGC Application Package used to deploy a new process.
    required: true
    content:
      application/ogcapppkg+json:
        schema:
          $ref: "_OGC_API_PROCESSES_SPECS_ROOT_/schemas/processes-dru/ogcapppkg.yaml"

'''
import yaml
import requests
import argparse

def deploy_app_pack(template_file, process_cwl_url, app_pack_registry):
    with open(template_file, 'r') as f:
        data = yaml.safe_load(f)


    if data["executionUnit"]["href"]:
        data["executionUnit"]["href"] = process_cwl_url

    # r = requests.post(app_pack_registry, data=data)

    # if r.ok:
    #     print("Application package successfully deployed.")
    # else:
    #     r.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy application package.")
    parser.add_argument("--process-cwl-url", type=str, help="URL to process CWL describing application package to deploy", required=True)
    parser.add_argument("--registry", type=str, help="Application package registry to deploy application package to.")
    parser.add_argument("--app-pack-template-file", type=str, default="ogc_app_pack/templates/ogcapppkg.yml", help="Path to the OGC API processes compliant OGC application package schema template.")

    args = parser.parse_args()

    print("Deploying application package: ", args)
    deploy_app_pack(process_cwl_url=args.process_cwl_url, app_pack_registry=args.registry, template_file=args.app_pack_template_file)