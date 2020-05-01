FROM python:3.6.9

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-pip

RUN pip3 install --upgrade pip && \
    pip3 install \
        numpy \
        matplotlib \
        scipy

CMD ["/bin/bash"]
