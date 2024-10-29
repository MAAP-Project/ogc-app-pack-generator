#!/usr/bin/env bash

set -ex

python3 generate_build_config.py algorithm_configs/algorithm_config.yaml

VERDI_HOME=/home/gitlab-runner/verdi
source ${VERDI_HOME}/bin/activate
source $PWD/config.txt
export SKIP_PUBLISH="noskip"
isSet=1

# Check for CI/CD Variables
for var in S3_CODE_BUCKET MOZART_URL GRQ_REST_URL
do
    if [ -z "${!var}" ]; then
        echo "${var} not set"
        isSet=""
    fi
done
if [ -z "${isSet}" ]; then
    echo "One or more variable is not set"
    exit 1
fi

echo 'Listing variables...'
echo ${REPO_NAME}
echo ${BRANCH}
echo ${S3_CODE_BUCKET}
echo ${MOZART_URL}
echo ${GRQ_REST_URL}
echo ${SKIP_PUBLISH}
echo ${CONTAINER_REGISTRY}
CACHE_BUST=$(date +%s)
echo 'End of listing variables'

${VERDI_HOME}/ops/container-builder/build-container.bash.app-pack ${REPO_NAME} ${BRANCH} ${S3_CODE_BUCKET} ${MOZART_URL} ${GRQ_REST_URL} ${SKIP_PUBLISH} ${CONTAINER_REGISTRY} --build-arg BASE_IMAGE_NAME=${BASE_IMAGE_NAME} --build-arg REPO_URL_WITH_TOKEN=${REPO_URL_WITH_TOKEN} --build-arg REPO_NAME=${REPO_NAME} --build-arg BRANCH=${BRANCH} --build-arg BUILD_CMD="${BUILD_CMD}" --build-arg CACHE_BUST=${CACHE_BUST}

deactivate
export ogc_container_url=$(tail -1 build_container_output.txt)
echo "$(basename ${ogc_container_url})" > container_url.txt
python3 generate_app_pack.py algorithm_configs/algorithm_config.yaml $(basename ${ogc_container_url})

curl -k --location --request POST "http://${WPST_API_URL}/processes" --header 'Content-Type: application/x-yaml' --data-binary @process.cwl