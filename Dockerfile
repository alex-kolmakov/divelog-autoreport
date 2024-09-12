FROM mageai/mageai:0.9.73
ARG PIP=pip3

ARG MAGE_CODE_PATH=/home/src

WORKDIR ${MAGE_CODE_PATH}

COPY . .
COPY divelog/requirements.txt .
RUN ${PIP} install --upgrade pip && ${PIP} install -r requirements.txt
RUN dlt --non-interactive init rest_api lancedb

WORKDIR ${MAGE_CODE_PATH}

ENV PYTHONPATH="${PYTHONPATH}:/home/src"

CMD ["/bin/sh", "-c", "/app/run_app.sh"]
