# OGC Application Package Generator
GitHub action to build OGC application packages compliant with CWL and OGC best practices.

This action accepts a YML file describing an algorithm as input and uses it to populate a CWL workflow template file to produce a workflow file. The generated workflow file is validated using `cwltool` and `ogc_ap_validator` to ensure it is compliant with CWL and OGC best practices before it is then committed to the working branch under `workflows/`. A docker image will be built from the user-specified Dockerfile and pushed to the working repo's GitHub Container Registry.

See `data/workflow_configuration.yml` for a sample YML input file.

See `workflows/process_sardem-sarsen_mlucas_nasa-ogc.cwl` for a sample workflow file generated from the `data/worklow_configuration.yml` input.

## Build OGC application package using GitHub actions

To use this action in a client repo, create a GitHub workflow file at the root of your repo:

`touch .github/workflows/my_workflow.yml`

Copy this workflow into the file that was just created and update where necessary:

```
on:
  push:
    branches:
      - `**`
jobs:
  build_app_pack:
    environment: DIT
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo content
        uses: actions/checkout@v4

      - name: Use OGC App Pack Generator Action
        uses: MAAP-Project/ogc-app-pack-generator@feature/create-action
        with:
          # Specify action inputs
          workflow-configuration-path: nasa/ogc/workflow_configuration.yml
          dockerfile-path: nasa/Dockerfile
```

The workflow is currently set to trigger on commits to any branch. To limit workflow triggering to a specific branch, replace `'**'` with your branch name.

The action currently accepts two inputs: the path to the workflow configuration YML and the path to the Dockerfile, both relative to the root of the working repo. Update these parameters to point to the workflow configuration and Dockerfile in your repo.

Once these updates are made, and the working repo's workflow is triggered, that will trigger generation of the OGC application package. The resulting CWL workflow file will be committed to the working branch under `workflows/` and the Docker image will be pushed to the repo's GHCR.


## Build CWL workflow file from the command line
Run the following to generate a CWL workflow file from the command line:

`python build_cwl_workflow.py --yaml-file data/workflow_configuration.yml`

This will create `workflows/process.cwl`.

To run CWL validation, install `cwltool` and run with the validation flag:
```
pip install cwltool &&
cwltool --validate workflows/process.cwl
```

To run OGC validation, install `ogc_ap_validator` and run the validation:
```
pip install ogc_ap_validator &&
ap-validator workflows/process.cwl
```

> [!NOTE]
> This script only builds the CWL and not the Docker image. Users will have to update the Docker requirements in the generated CWL to point to an existing image.

## Run CWL workflow
Sample command to run a workflow. Be sure to provide any required inputs:

`cwltool workflows/process.cwl --input_1 "input1" --input_2 "input2"`
