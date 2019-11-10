# Global Fashion Group Data Science Challenge - Karthik's entry

## Overview
I have built my code using the Kedro framework. Take a look at the [documentation](https://kedro.readthedocs.io) to get started.
Project was initialised in `Kedro 0.15.4` by running:
```
kedro new
```
## Things to note
 * No data was commited to this repo.
 * No credentials was commited to this repo. All credentials should be created by the user in a `credentials.yml` file and stored in `conf/local/`

## Overview of pipeline
![Pipeline](./data/08_reporting/pipeline.png)

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