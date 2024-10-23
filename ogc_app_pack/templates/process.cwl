cwlVersion: v1.0
$graph:
- class: Workflow
  label: ALGORITHM_NAME
  doc: ALGORITHM_DESCRIPTION
  id: ALGORITHM_ID
  inputs:
    INPUT_NAME:
      type: INPUT_TYPE
      label: INPUT_LABEL
      doc: INPUT_DESCRIPTION
      default: INPUT_DEFAULT
  outputs:
    output_context:
      type: Directory
      outputSource: process/job_output
  steps:
    process:
      run: "#process"
      in:
        INPUT_NAME: INPUT_NAME
      out: [job_output]
- class: CommandLineTool
  id: process
  requirements:
    DockerRequirement:
      dockerPull: DOCKER_URL
  baseCommand: RUN_COMMAND
  arguments: []
  inputs:
    INPUT_NAME:
      type: INPUT_TYPE
      inputBinding:
        position: 1
  outputs:
    job_output:
      type: Directory
      outputBinding:
        glob: output*
$namespaces:
  s: https://schema.org/
s:softwareVersion: 1.0.0
schemas:
- http://schema.org/version/9.0/schemaorg-current-http.rdf
