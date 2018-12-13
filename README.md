# dl-project

[![Build Status](https://travis-ci.org/bjk17/dl-project.svg?branch=master)](https://travis-ci.org/bjk17/dl-project)

Teaching a Deep Neural Network to solve simple chess endgames solely with Reinforcement Learning.


## Dependencies
```bash
pip install -r requirements.txt

# macOS local development (included in Google Colaboratory)
pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.12.0-py3-none-any.whl
```

## Generate self-play data

```bash
mkdir -p trainingdata/
python selfplay.py trainingdata/batch1.txt 100 models/v1.h5 models/v2.h5 0.0 [random_seed]
```