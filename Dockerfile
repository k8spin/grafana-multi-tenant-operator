FROM python:3.12

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

COPY handler.py /src/handler.py
COPY grafana /src/grafana

CMD kopf run /src/handler.py --verbose --log-format full
