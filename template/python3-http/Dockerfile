ARG PYTHON_VERSION=3.12
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/of-watchdog:0.10.7 AS watchdog
FROM --platform=${TARGETPLATFORM:-linux/amd64} python:${PYTHON_VERSION}-alpine AS build

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG UPGRADE_PACKAGES
ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)

RUN if [ "${UPGRADE_PACKAGES}" = "true" ] || [ "${UPGRADE_PACKAGES}" = "1" ]; then apk --no-cache upgrade; fi && \
    apk --no-cache add ${ADDITIONAL_PACKAGE}

# Add non root user
RUN addgroup -S app && adduser app -S -G app
RUN chown app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/

COPY --chown=app:app index.py           .
COPY --chown=app:app requirements.txt   .
USER root
RUN pip install --no-cache-dir -r requirements.txt

# Build the function directory and install any user-specified components
USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY --chown=app:app function/requirements.txt	.
RUN pip install --no-cache-dir --user -r requirements.txt

# install function code
USER root
COPY --chown=app:app function/   .

FROM build AS test
ARG TEST_COMMAND=tox
ARG TEST_ENABLED=true
RUN [ "$TEST_ENABLED" = "false" ] && echo "skipping tests" || eval "$TEST_COMMAND"

FROM build AS ship
WORKDIR /home/app/

# configure WSGI server and healthcheck
USER app

ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
