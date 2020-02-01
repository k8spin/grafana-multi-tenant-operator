FROM python:3.7

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY handler.py /src/handler.py
COPY grafana /src/grafana

CMD kopf run /src/handler.py --verbose
