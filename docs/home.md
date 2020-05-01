# UMICH NCLT SLAP Documentation <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Contributors](#contributors)
- [Project Resources](#project-resources)
- [Dataset](#dataset)
- [Libraries](#libraries)
- [Docker](#docker)
  - [Install & Setup](#install--setup)
  - [Running Container](#running-container)
- [Documentation](#documentation)
  - [Semantic Language Parsing: Chatbot](#semantic-language-parsing-chatbot)
  - [Particle Filter](#particle-filter)

## Contributors

### Project Team <!-- omit in toc -->

- Sravan Balaji ([balajsra@umich.edu](mailto:balajsra@umich.edu))
- Sabrina Benge ([snbenge@umich.edu](mailto:snbenge@umich.edu))
- Dwight Brisbin ([dbrisbin@umich.edu](mailto:dbrisbin@umich.edu))
- Hao Zhang ([hzha@umich.edu](mailto:hzha@umich.edu))
- Yushu Zhang ([yushuz@umich.edu](mailto:yushuz@umich.edu))

### EECS 568 / NAVARCH 568 / ROB 530 W20 Course Staff <!-- omit in toc -->

- Maani Ghaffari ([maanigj@umich.edu](mailto:maanigj@umich.edu))
- Tzu-Yuan (Justin) Lin ([tzuyuan@umich.edu](mailto:tzuyuan@umich.edu))
- Peter Westra ([pwestra@umich.edu](mailto:pwestra@umich.edu))

## Project Resources
- [Repository](https://github.com/Mobile-Robotics-W20-Team-9/UMICH-NCLT-SLAP)
- [Video Summary](https://youtu.be/4xinp3mZIP0)
- [Presentation from Video](https://docs.google.com/presentation/d/1PUHZjGNijsOMJ2KPXF_PAGO-eqZTLd085ZuNPc3VSsI/edit?usp=sharing)
- [Generated Models from NCLT Data](https://drive.google.com/drive/folders/1cFf0q76xyul4nbShm-GwDNxFwYh1Bkzx?usp=sharing)
- [Project Report](https://www.overleaf.com/read/ktshtqzyzmxt)

## Dataset

[The University of Michigan North Campus Long-Term Vision and LIDAR Dataset](http://robots.engin.umich.edu/nclt/)

## Libraries

- [NumPy](https://numpy.org/)
- [Scipy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [NLTK](https://pypi.org/project/nltk/)
- [Spacy](https://pypi.org/project/spacy/)
- [Pickle](https://pypi.org/project/pickle-mixin/)
- [TensorFlow](https://pypi.org/project/tensorflow/)
- [Keras](https://pypi.org/project/Keras/)

## Docker

### Install & Setup

For instructions on installing and setting up Docker, see [Getting Started with Docker](https://sravanbalaji.com/Web%20Pages/blog_docker.html) on Sravan's website.

### Running Container

After cloning the repo, start your docker machine and following commands shown below in your docker terminal.

1. `cd /PATH/TO/UMICH_NCLT_SLAP/docker`
2. `docker-compose run --rm <service>`

## Documentation

### Semantic Language Parsing: Chatbot

For standalone testing of the chatbot, run the following commands

1. `cd /PATH/TO/UMICH_NCLT_SLAP/docker`
2. `docker-compose run --rm semantic`
3. `cd app/semantic`
4. `python gui_chatbot.py`

You can update the models by changing the intent or pickle files. Intent.json can be changed with a basic text editor and pickles can be read and changed using pickleManage.py.

1. `cd /PATH/TO/UMICH_NCLT_SLAP/src/dataset/dataManipulation/pickles`
2. `python`
3. `from pickleManage import *`
4. Use desired functions. Functions are documented with examples in pickleManage.py file. To update the models are making changes run: `python` 

### Particle Filter

To run particle filter you have to use python 2.7. 
Install the following dependencies

1. `sudo apt install python-pip python-tk`
2. `pip install numpy matplotlib open3d-python progressbar pyquaternion transforms3d scipy scikit-image networkx psutil`
3. Install required dependencies including ray_tracing, pybind11, pytest, and Catch2
 `git clone https://github.com/catchorg/Catch2.git`
 
 `mkdir Catch2/build`
 
 `cd Catch2/build`
 
 `cmake ..`
 
 `make -j8`
 
 `sudo make install`


 `pip install pytest`


 `git clone https://github.com/pybind/pybind11.git`
 
 `mkdir pybind11/build`
 
 `cd pybind11/build`
 
 `cmake ..`
 
 `make -j8`
 
 `sudo make install`


`git clone https://github.com/acschaefer/ray_tracing.git`

`mkdir ray_tracing/build && cd ray_tracing/build`

`cmake ..`

`make -j8`

`sudo make install`

4. Download raw data from [NCLT](http://robots.engin.umich.edu/nclt/) to run code from scratch OR use our [prebuilt maps](https://drive.google.com/drive/folders/1cFf0q76xyul4nbShm-GwDNxFwYh1Bkzx?usp=sharing)

4.1 The raw data can be downloaded from the website directly or using the downloader.py. If you are using the prebuilt maps, skip this step. 

`cd src/dataset/`

`python download.py --date="2012-01-15" --vel --gt --gt_cov --sensor`

`cd nclt/sensors/<date>`

`tar xzf <sensors_file>`

`cd ../velodyne`

`tar xzf <velodyne_file>`

Repeat this for any interested datasets. We have maps made for 2012-01-15, 2012-01-08, 2013-04-05, and 2013-01-10.

5. In ncltpoles.py we need to make a couple changes
`cd src/polex/poles/`  

Open and edit ncltpoles.py with your favorite editor.
There are two # TODO comments. In the first one change 2020-04 to <year>-<month>. In the second one change the session to your desired session date. If you would like to run the exact experiment we did, do not change this date.
 
 6. In pynclt.py we need to make a couple changes
 `cd src/polex/poles`
 
 Open and edit pynclt.py with your favorite editor.
 There are two # TODO comments. In the first one, change paths to the appropriate directories on your machine. In the second one, comment our the sessions you are not using. 
 
 7. Run it. WARNING this can take anywhere from 1 - 10 hours for 4 datasets. 
 `cd src/polex/poles`
 
 `python2 ncltpoles.py`
 
### Motion Planning

1. `cd src/dataset`
2. `python download.py --date="2012-01-08" --gt`
3. `cd ../planning`
4. `python astar_demo.py`
4.1. This saves the path as path.npy and generates an image, astar_path.png
5. `python twist_demo.py`
5.1. Does not produce output
6. `interpolation.py`
6.1. Produces a plot of smoothed position and velocity. 
