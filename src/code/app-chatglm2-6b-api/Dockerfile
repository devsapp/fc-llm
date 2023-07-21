
FROM  nvidia/cuda:12.1.0-runtime-ubuntu20.04

USER root

ENV ROOT=/mnt/auto/chatglm

ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8089

LABEL MAINTAINER="FC"

RUN mkdir -p ${ROOT}
COPY ./requirements.txt /mnt/auto/chatglm/requirements.txt


WORKDIR ${ROOT}

RUN apt-get update -y && apt-get install -y tzdata && apt-get install python3 python3-pip curl -y

RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN apt-get install -y nvidia-container-toolkit-base && apt-get install libgl1-mesa-glx -y

RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && apt-get clean

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py 

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com && rm -rf `pip3 cache dir`



EXPOSE ${PORT}


CMD ["python3","-u", "main.py"]