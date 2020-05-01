# UMICH NCLT SLAP Documentation <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->
- [Contributors](#contributors)
- [Dataset](#dataset)
- [Libraries](#libraries)
- [Docker](#docker)
  - [Install & Setup](#install--setup)
  - [Running Container](#running-container)

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

## Dataset

[The University of Michigan North Campus Long-Term Vision and LIDAR Dataset](http://robots.engin.umich.edu/nclt/)

## Libraries

- [OpenCV](https://opencv.org/)
- [Point Cloud Library](http://pointclouds.org/)
- [NumPy](https://numpy.org/)
- [Scipy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Natural Language Toolkit](https://www.nltk.org/)
- [Cpython](https://pypi.org/project/cPython/)
- [NLTK](https://pypi.org/project/nltk/)
- [Setup Tools](https://pypi.org/project/setuptools/)
- [Pylint](https://pypi.org/project/pylint/)
- [Spacy](https://pypi.org/project/spacy/)
- [Pickle](https://pypi.org/project/pickle-mixin/)
- [TensorFlow](https://pypi.org/project/tensorflow/)
- [Keras](https://pypi.org/project/Keras/)

## Docker

### Install & Setup

For instructions on installing and setting up Docker, see [Getting Started with Docker](https://sravanbalaji.com/Web%20Pages/blog_docker.html) on Sravan's website.

### Running Container

After cloning the repo, start your docker machine and following commands shown below in your docker terminal.

1. `cd /PATH/TO/UMICH_NCLT_SLAP/src`
2. `docker-compose run --rm python-dev`

### Semantic Language Parsing: Chatbot

For standalone testing of the chatbot, run the following commands

1. `cd /PATH/TO/UMICH_NCLT_SLAP/semantic/src`
2. `docker-compose run --rm python-dev`
1. `cd app/semantic`
2. `python gui_chatbot.py`

You can update the models by changing the intent or pickle files. Intent.json can be changed wiht a basic text editor and pickles can be read and changed using pickleManage.py.
1. `cd /PATH/TO/UMICH_NCLT_SLAP/src/datset/dataManipulation/pickles`
2. `python`
3. `from pickleManage import *`
4. Use desired functions. Functions are documented with examples in pickleManage.py file.
To update the models are making changes run:
'python 


### Velocity Control: MPC
Even though the velocity control is not finally integrated into the whole navigation, you can still run it for short-term trajectory tracking combined with A* algorithm. There are two demos can be tested: single-round demo and the mpc along the whole trajectory. Both of them require a .csv file which includes the ground-truth poses of the whole graph map.
Run the following commands to test:
1. `cd  /PATH/TO/UMICH_NCLT_SLAP/src/control`
2. `docker-compose run --rm python-dev`
3. `python one_round_demo.py /PATH TO YOUR .csv FILE` or `python mpc_along_trajectory.py /PATH TO YOUR .csv FILE`

