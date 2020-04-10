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

## Docker

### Install & Setup

For instructions on installing and setting up Docker, see [Getting Started with Docker](https://sravanbalaji.com/Web%20Pages/blog_docker.html) on Sravan's website.

### Running Container

After cloning the repo, start your docker machine and following commands shown below in your docker terminal.

1. `cd /PATH/TO/UMICH_NCLT_SLAP/src`
2. `docker-compose run --rm python-dev`
