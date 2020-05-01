FROM python:3

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python-dev \
        python-pip \
        libpython2.7-dev \
        python3-dev \
        python3-pip \
        python-tk \
        libgl1-mesa-glx \
        git \
        cmake

RUN pip2 install --upgrade pip && \
    pip2 install \
        numpy \
        matplotlib \
        open3d-python \
        progressbar2 \
        pyquaternion \
        transforms3d \
        scipy \
        scikit-image \
        networkx \
        psutil \
        torch \
        future

RUN mkdir /app

# Catch2
RUN cd /app && \
    git clone https://github.com/catchorg/Catch2.git && \
    mkdir -p /app/Catch2/build && \
    cd /app/Catch2/build && \
    cmake .. && \
    make -j8 && \
    make install

RUN python3.8 -m pip install pytest

# pybind11
RUN cd /app && \
    git clone https://github.com/pybind/pybind11.git && \
    mkdir -p /app/pybind11/build && \
    cd /app/pybind11/build && \
    cmake .. && \
    make -j8 && \
    make install

# ray tracing
RUN cd /app && \
    git clone https://github.com/acschaefer/ray_tracing.git && \
    mkdir -p /app/ray_tracing/build && \
    cd /app/ray_tracing/build && \
    cmake .. && \
    make -j8 && \
    make install

RUN pip2 uninstall -y backports.functools-lru-cache && \
    apt-get install python-backports.functools-lru-cache

ENV PYTHONPATH=$PYTHONPATH:/app/ray_tracing/python

CMD ["/bin/bash"]
