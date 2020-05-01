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
  - [Motion Planning](#motion-planning)
  - [Velocity Control: MPC](#velocity-control-mpc)

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

To run particle filter, you can use the provided Dockerfile.

1. `cd /PATH/TO/UMICH_NCLT_SLAP/docker`
2. `docker-compose run --rm particle-filter`
3. Download data
   1. Download raw data from [NCLT](http://robots.engin.umich.edu/nclt/) to run code from scratch
      - The raw data can be downloaded from the website directly or using the downloader.py inside the docker container
      - `cd /app/dataset/data`
      - `python download.py --date="2012-01-15" --vel --gt --gt_cov --sensor`
      - `cd /app/datasset/data/sensor_data/<date>`
      - `tar xzf <sensors_file>`
      - `cd ../velodyne_data`
      - `tar xzf <velodyne_file>`
   2. OR use our [prebuilt maps](https://drive.google.com/drive/folders/1cFf0q76xyul4nbShm-GwDNxFwYh1Bkzx?usp=sharing)
   3. Repeat this for any interested datasets. We have maps made for 2012-01-15, 2012-01-08, 2013-04-05, and 2013-01-10.
4. In ncltpoles.py we need to make a couple changes
   - `cd src/polex/poles/`
5. Open and edit ncltpoles.py with your favorite editor. There are two `TODO` comments. In the first one change 2020-04 to <year>-<month>. In the second one change the session to your desired session date. If you would like to run the exact experiment we did, do not change this date.
6. In pynclt.py we need to make a couple changes
   - `cd src/polex/poles`
7. Open and edit pynclt.py with your favorite editor. There are two `TODO` comments. In the first one, change paths to the appropriate directories on your machine. In the second one, comment our the sessions you are not using.
8. Run it. WARNING this can take anywhere from 1 - 10 hours for 4 datasets. 
   - `cd src/polex/poles`
   - `python2 ncltpoles.py`
 
### Motion Planning

1. `cd /PATH/TO/UMICH_NCLT_SLAP/docker`
2. `docker-compose run --rm planning`
3. `cd /app/dataset/data`
4. `python download.py --date="2012-01-08" --gt`
5. `cd /app/planning`
6. `python astar_demo.py`
   - This saves the path as path.npy and generates an image, astar_path.png
7. `python twist_demo.py`
   - Does not produce output
8. `interpolation.py`
   - Produces a plot of smoothed position and velocity. 

### Velocity Control: MPC

Even though the velocity control is not finally integrated into the whole navigation, you can still run it for short-term trajectory tracking combined with A* algorithm. There are two demos can be tested: single-round demo and the mpc along the whole trajectory. Both of them require a .csv file which includes the ground-truth poses of the whole graph map.

Run the following commands to test:

1. `cd /PATH/TO/UMICH_NCLT_SLAP/src/control`
2. `docker-compose run --rm velocity-control`
3. `python one_round_demo.py /PATH/TO/YOUR/.csv_FILE` or `python mpc_along_trajectory.py /PATH/TO/YOUR/.csv_FILE`
