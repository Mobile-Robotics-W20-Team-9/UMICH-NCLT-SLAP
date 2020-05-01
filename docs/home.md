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

<!-- TODO: Add instructions for running particle filter code -->