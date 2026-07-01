# OGC Application Package Generator
GitHub action to build OGC application packages compliant with CWL and OGC best practices.

This action builds a CWL workflow file from an input YAML file. The CWL workflow file is validated using `cwltool` and `ogc_ap_validator` to ensure it is compliant with CWL and OGC best practices. It is then committed to the client repository's working branch under `cwl_workflows/`. A docker image will be built from the user-specified Dockerfile and pushed to the client repository's GitHub Container Registry.

See `data/algorithm_config.yml` for a sample YAML input file.

See `data/process_sardem-sarsen_mlucas_nasa-ogc.cwl` for a sample workflow file generated from the `data/algorithm_config.yml` input.

> [!IMPORTANT]
> This action **writes to your repository**. On each run it commits the generated CWL workflow file to `cwl_workflows/` on the triggering branch and pushes the commit back using the workflow's `GITHUB_TOKEN`. It also builds and pushes a Docker image to your repository's GitHub Container Registry (when `dockerfile-path` is set). Because of this, the calling workflow must grant `contents: write` and `packages: write` permissions (see the sample below), and the action must run on a branch it is allowed to push to. Do not use this action on untrusted pull requests.

## Build OGC application package using GitHub actions

To use this action in a client repository, create a GitHub workflow file at the root of your repository:

`touch .github/workflows/my_workflow.yml`

Copy the sample workflow below into `my_workflow.yml` and be sure to change the action inputs if needed.

> [!NOTE]
> Your workflow **must check out the repository** (with `actions/checkout`) in a step before invoking this action, as shown below. The action operates on the checked-out working tree and pushes the generated workflow file back to it.

```
on:
  push:
    branches:
      - '**'
jobs:
  build_app_pack:
    environment: DIT
    runs-on: ubuntu-latest

    permissions:
      contents: write
      packages: write

    steps:
      - name: Checkout repo content
        uses: actions/checkout@v4

      - name: Use OGC App Pack Generator Action
        uses: MAAP-Project/ogc-app-pack-generator@main
        with:
          # Specify action inputs
          algorithm-configuration-path: nasa/ogc/algorithm_config.yml
          dockerfile-path: nasa/Dockerfile
          deploy-app-pack: true
          app-pack-register-endpoint: https://api.dit.maap-project.org/api/ogc/processes
        env:
          # MAAP token is required to deploy the process
          MAAP_TOKEN: ${{ secrets.MAAP_TOKEN_MLUCAS }}
```

### Action Inputs:

| Parameter        | Description           | Required | Default | Type  |
|:-------------:|:---------------------:|:-----:|:-----:|:-----:|
| algorithm-configuration-path | Path to the algorithm configuration YAML file | Yes | - | string ex. `nasa/ogc/algorithm_config.yml` |
| dockerfile-path | Path to the Dockerfile used to build the algorithm image. Omit if `algorithm_container_url` is set in the config file (the two are mutually exclusive). | No | - | string ex. `nasa/Dockerfile` |
| deploy-app-pack | Whether to deploy the application package to a registry | No | `false` | boolean ex. `true` |
| app-pack-register-endpoint | Deployment request URL for the application package registry. Required when `deploy-app-pack` is `true`. | No | - | string ex. `https://api.dit.maap-project.org/api/ogc/processes` |

> [!NOTE]
> To use a prebuilt container image instead of building one from a Dockerfile, set `algorithm_container_url` in the algorithm configuration YAML file and omit `dockerfile-path`. Exactly one of the two must be provided.

### Environment variables:

| Variable | Description | Required |
|:-------------:|:---------------------:|:-----:|
| MAAP_TOKEN | Auth token sent with the deployment request (as the `proxy-ticket` header). Only needed when `deploy-app-pack` is `true`. Pull it from the client repository's secrets store as shown in the sample workflow above. | Conditional |

> [!NOTE]
> The workflow is currently set to trigger on a push to any branch. To limit workflow triggering to a specific branch, replace `'**'` with your branch name.

## Build CWL workflow file from the command line
Run the following to generate a CWL workflow file from the command line:

`python build_cwl_workflow.py --config-file data/algorithm_config.yml`

This will create `cwl_workflows/process.cwl`.

To run CWL validation, install `cwltool` and run with the validation flag:
```
pip install cwltool &&
cwltool --validate cwl_workflows/process.cwl
```

To run OGC validation, install `ogc_ap_validator` and run the validation:
```
pip install ogc_ap_validator &&
ap-validator cwl_workflows/process.cwl
```

The OGC validator has an option to return the validation results in json format by adding the `--format` flag. For example:
```
ap-validator --format json cwl_workflows/process.cwl
```

Here is a sample response indicating the CWL is OGC-compliant:
```
{
  "valid": true,
  "issues": [],
  "requirements": {}
}
```

Here is a sample response indicating the CWL is NOT OGC-compliant:
```
{
  "valid": false,
  "issues": [
    {
      "type": "error",
      "message": "Missing element for Workflow 'sardem-sarsen': doc",
      "req": "req-9"
    }
  ],
  "requirements": {
    "req-9": "The Application Package CWL Workflow class SHALL contain the following elements: Identifier ('id'); Title ('label'); Abstract ('doc')."
  }
}
```

> [!NOTE]
> If running this script outside of the GitHub action, it will only generate the CWL and not the Docker image. Users will have to update the Docker requirements in the generated CWL to point to an existing image if they wish to execute the workflow.

## Run CWL workflow
Sample command to execute a workflow. Be sure to provide any required inputs:

`cwltool cwl_workflows/process.cwl --input_1 "input1" --input_2 "input2"`

Inputs may also be provided as a YAML file, for example:

`cwltool cwl_workflows/process.cwl data/input.yml`

See `data/input.yml` for a sample YAML input file.

