FROM openfaas/of-watchdog:0.5.3 as watchdog
FROM python:2.7-alpine

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

ARG ADDITIONAL_PACKAGE
# Alternatively use ADD https:// (which will not be cached by Docker builder)
RUN apk --no-cache add ${ADDITIONAL_PACKAGE}

WORKDIR /root/

COPY requirements.txt   .
RUN pip install -r requirements.txt
COPY index.py           .

RUN mkdir -p function
RUN touch ./function/__init__.py
WORKDIR /root/function/
COPY function/requirements.txt	.
RUN pip install -r requirements.txt

WORKDIR /root/
COPY function           function

ENV fprocess="python index.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"


HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]
