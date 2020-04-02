FROM openfaas/classic-watchdog:0.18.1 as watchdog
FROM python:3.7
COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apt-get update \
    && apt-get install -y ca-certificates ${ADDITIONAL_PACKAGE} \
    && rm -rf /var/lib/apt/lists/

# Add non root user
RUN groupadd app && useradd -r -g app app

RUN mkdir -p /home/app && chown -R app /home/app && \
    mkdir -p /home/app/python && chown -R app /home/app

USER app

ENV PATH=$PATH:/home/app/.local/bin:/home/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/home/app/python

WORKDIR /home/app/

COPY index.py           .
COPY requirements.txt   .
USER root
RUN pip install -r requirements.txt --target=/home/app/python
USER app

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /home/app/function/
COPY function/requirements.txt .
RUN pip install -r requirements.txt --target=/home/app/python

WORKDIR /home/app/

USER root
COPY function   function
RUN chown -R app:app ./ && \
    chmod -R 777 /home/app/python

USER app

# Set up of-watchdog for HTTP mode
ENV fprocess="python3 index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
