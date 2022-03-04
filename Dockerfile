FROM python:3.7

ENV HF_INFERENCE_URL=http://tchen.xyz:33960/

WORKDIR /workdir
COPY . ./

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

ENTRYPOINT gunicorn -b 0.0.0.0:80 app:app
