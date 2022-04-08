FROM python:3.7

# Deploy your own! See https://github.com/tianle91/hf-inference
ENV HF_INFERENCE_URL=http://vpn.tchen.xyz:33960/

WORKDIR /workdir
COPY . ./

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
