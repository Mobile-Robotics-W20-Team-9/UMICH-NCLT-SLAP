FROM python:3

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python-opencv \
        libpcl-dev

RUN pip install -U pip && \
    pip install -U \
        cython \
        numpy \
        scipy \
        matplotlib \
        nltk \
        setuptools

CMD ["/bin/bash"]