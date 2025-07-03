cwlVersion: v1.2
$graph:
  - class: Workflow
    label: null 
    doc: null
    id: null
    inputs: null
    outputs: null
    steps:
      process:
        run: "#main"
        in: null
        out: null

  - class: CommandLineTool
    id: main
    requirements:
      DockerRequirement:
        dockerPull: null
      NetworkAccess:
        networkAccess: true
      ResourceRequirement:
        ramMin: null
        coresMin: null
        outdirMax: null
    baseCommand: null
    inputs: null
    outputs: null

s:author:
  - class: s:Person
    s:name: null

s:contributor:
  - class: s:Person
    s:name: null

s:citation: null
s:codeRepository: null
s:commitHash: null
s:dateCreated: null
s:license: null
s:softwareVersion: null
s:version: null
s:releaseNotes: null
s:keywords: null

$namespaces:
  s: https://schema.org/

$schemas:
- https://raw.githubusercontent.com/schemaorg/schemaorg/refs/heads/main/data/releases/9.0/schemaorg-current-http.rdf