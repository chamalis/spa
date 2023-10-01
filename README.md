# SPA

SPA is a simple movie REST API to demonstrate
minimal usage of FastAPI with PostgreSQL, SQLAlchemy,
Docker, Nginx. 

It may serve as a template for FastAPI
projects.

It uses the datasets found here: 

* https://datasets.imdbws.com/title.basics.tsv.gz
* https://datasets.imdbws.com/title.ratings.tsv.gz

and has no interface so far. 

## Configuration file

COPY `env.example.native` or `env.example.docker` to `.env`
and FILL IN according to your environment. Default values
will probably work, but its recommended to verify yourself.

In order to switch from host to docker and vice versa,
the `.env` needs to be changed accordingly every time.
Theoretically in this version, the only parameter that should
need to change is 

* `DB_HOST`
  * For docker: `DB_HOST=spa_db`
  * For host: `DB_HOST=127.0.0.1` 
 or the IP where the postgresql server is running

## Docker deployment

Prerequisites:
* docker
* docker-compose

```commandline
docker-compose build && docker-compose up -d
```

First time it runs, it will create the db
and fill in data which will take several 
minutes. Please do not interrupt it during that stage.

## Native deployment (non-docker)

### Prerequisites: ###
* Python3 (tested at 3.10.12)
* python3-virtualenv


### Python Virtual env setup

You can Replace `venv` with any writtable path:

```commandline
virtualenv -p python3 venv
source venv/bin/activate
```

### Update PYTHONPATH

assuming you have cd in `spa` folder

```commandline
export PYTHONPATH=$PYTHONPATH:$(pwd)/app
```

#### Install dependencies

```commandline
pip install -r requirements/dev.txt
```


### Download data

The following script downloads the relevant .tsv.gz files
into the `raw_data` directory if not already there

```bash
./scripts/prepare_data.sh
```

### create db

This step needs postgresql server and client to be installed

Using the same data you use in `.env`
e.g, create db `spa` using postgres user `spa`:

```commandline
createdb -U spa spa
```

### init db

Create the schema

```commandline
alembic upgrade head
```

WARNING: The following script (fills in the DB) will take 5-15 minutes:

```bash
python ./scripts/populate_db.py
```

if there are (real) data already in, it will fail with an IntegrityError
(due to primary keys uniqueness)

### run
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Example Usage

Rather than using curl, I 'd suggest to use Firefox, for the GET requests, 
since it has builtin json viewer. 

Here we assume  the host is `localhost` and port `8000`.


```bash
# create via imdb_url
curl -i --header "Content-Type: application/json"  -X POST -d '{"title": "Incendies", "imdb_url":"https://www.imdb.com/title/tt1255953/"}'  http://127.0.0.1:8000/api/v1/movies

# create via imdb_url
curl -i --header "Content-Type: application/json"  -X POST -d '{"title": "Incendies", "imdb_id":"tt1255953"}'  http://127.0.0.1:8000/api/v1/movies

# get mystery sorted by best rating
curl -i -X GET http://127.0.0.1:8000/api/v1/movies?order=rating,desc&genre=Mystery

# next page based on the given ordering
curl -i -X GET http://127.0.0.1:8000/api/v1/movies?order=rating,desc&genre=Mystery&page=2

# Get Dramas with rating >= 8.6 ordered by title
curl -i -X GET http://127.0.0.1:8000/api/v1/movies?rating=8.6&genre=Drama&order=title

# Specify page size and page number
curl -i -X GET http://127.0.0.1:8000/api/v1/movies?page=4&size=66
```
