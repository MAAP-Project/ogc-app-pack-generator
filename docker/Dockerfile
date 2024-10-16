ARG BASE_IMAGE_NAME
FROM ${BASE_IMAGE_NAME}

USER root
WORKDIR /app

ARG REPO_URL_WITH_TOKEN
ARG REPO_NAME
ARG BRANCH
ARG BUILD_CMD

RUN git clone ${REPO_URL_WITH_TOKEN} && \
    cd ${REPO_NAME} && \
    git checkout ${BRANCH} && \
    chmod -R 775 .

RUN bash ${BUILD_CMD} && conda clean -afy

CMD ["/bin/bash"]
