# dl-project

[![Build Status](https://travis-ci.org/bjk17/dl-project.svg?branch=master)](https://travis-ci.org/bjk17/dl-project)

Teaching a Deep Neural Network to solve simple chess endgames solely with Reinforcement Learning.

## Generate self-play data

```bash
mkdir -p trainingdata/
python selfplay.py trainingdata/batch1.txt 100 models/v1.h5 models/v2.h5 [random_seed]
```