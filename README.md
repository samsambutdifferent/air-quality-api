# air-quality-api

Thank you for taking the time to review my submission, below please see setup and run instructions, overview of the architecture, comments on technical choices as well as the answer to the required question. I have tried to lay the project out in a way that is clear and extendable.


## Data

Have chosen to use the netCDF file. The netCDF file is prepared as a parquet file for load into pandas. See the [data readme](./data/read_data.md) for info on running


## Setup

### Local Setup


```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Run:

```bash
python run.py
```

Test:

```bash
python -m pytest
```

### Docker

```bash
docker build -t air-quality-api .
docker run -p 5000:5000 air-quality-api
```


### Styling

Formatter:

```bash
black .
```

Type checker:

```bash
mypy app
```

### Documentation


```bash
python run.py
```

Go to -> `http://127.0.0.1:5000/api/`


### logging

Basic logging added, files in `./logs`, only added basic error logging


### Test coverage

```bash
coverage run -m pytest
coverage report

e.g.
----------------------------------------------------------
app/__init__.py                           19      0   100%
app/data_set.py                           24      0   100%
app/logger.py                             19      1    95%
app/routes.py                             87      3    97%
tests/functional/test_routes_func.py     176      0   100%
tests/unit/test_data_set.py               54      0   100%
----------------------------------------------------------
TOTAL                                    379      4    99%
```


## Architectire

```bash
./
│
├── app/
│   ├── __init__.py
│   ├── routes.py        
├── tests/   
│   ├── functional
            ....         
│   ├── unit           
            ....
├── run.py            
```

Application follows a modular architecture with a clear separation of concerns, utilising factory pattern



