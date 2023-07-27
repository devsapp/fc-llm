# docker build -f http.Dockerfile -t model_service_http:latest . --platform linux/amd64

FROM  nvidia/cuda:12.1.0-runtime-ubuntu20.04

USER root

ENV ROOT=/mnt/auto/model_service_http

ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8089

LABEL MAINTAINER="Buer"

RUN mkdir -p ${ROOT}
COPY ./requirements.txt /mnt/auto/model_service_http/requirements.txt

# COPY . /docker/

WORKDIR ${ROOT}

RUN apt-get update -y && apt-get install -y tzdata && apt-get install python3 python3-pip curl -y

RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get install -y nvidia-container-toolkit-base && apt-get install libgl1-mesa-glx -y

RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && apt-get clean

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py 

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com && rm -rf `pip3 cache dir`

# RUN chmod +x /docker/entrypoint.sh

EXPOSE ${PORT}

# ENTRYPOINT ["/docker/entrypoint.sh"]

CMD ["python3","-u", "http_server.py"]