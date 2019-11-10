# Global Fashion Group Data Science Challenge - Karthik's entry

## Overview
My focus in this challenge is to demonstrate project structuring, coding and data science fundamentals while optimising for simplicity over accuracy.
Hence please do not expect to find a kaggle-like deep-dive into the data and model tuning.
The project pipelines was built using Kedro and it allows running of entire pipelines, containerizing through docker and scheduling through airflow.
I have built my code using the Kedro framework. Take a look at the [documentation](https://kedro.readthedocs.io) to get started.
Project was initialised in `Kedro 0.15.4` by running:
```
kedro new
```
The bulk of the source code is in `src/gfg/pipeline.py`, `src/gfg/nodes/data_engineering.py` and `src/gfg/nodes/data_science.py`.
Data catalog is specified in `conf/base/catalog.yml` and training parameters are in `conf/base/parameters.yml`.
Final submission is in `data/07_model_output/submission.csv`.
## Things to note
 * No data was commited to this repo.
 * No credentials was commited to this repo. All credentials should be created by the user in a `credentials.yml` file and stored in `conf/local/`

## Overview of pipeline
![Pipeline](https://github.com/penguinpompom/gfg/blob/master/data/08_reporting/pipeline.PNG)

## Steps to run pipeline
1. Clone repo
2. Create new conda environment e.g:

```
conda create -n gfg 
```

2. Install kedro
```
pip install kedro
```

3. Install dependencies. Dependencies should be declared in `src/requirements.txt` for pip installation. To install them, run:
```
kedro install
```
4. Create a `credentials.yml` file in `conf/local/` with the following:
```
zip:
  password: <the password you provided>
```
5. Put the provided data set `test_data.zip` in `data/01_raw/`
4. Finally, run the Kedro project with:
```
kedro run
```
5. (Optional) Run the following command to render the kedro pipeline in a browser:
```
kedro viz
```
