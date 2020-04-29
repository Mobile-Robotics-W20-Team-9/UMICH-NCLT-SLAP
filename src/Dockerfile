FROM python:3

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python-opencv \
        libpcl-dev \
        x11-apps

RUN pip install -U pip && \
    pip install -U \
        cython \
        numpy \
        scipy \
        matplotlib \
        nltk \
        setuptools \
        pylint \
<<<<<<< HEAD
        pickle-mixin \
        spacy \
        --upgrade setuptools \
        --no-cache-dir tensorflow \
        keras

RUN python -m spacy download en_core_web_sm
=======
        pickle-mixin
>>>>>>> origin/master

CMD ["/bin/bash"]
