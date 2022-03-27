# Musical Work

## Development

### Using Docker Compose

#### 1- Environment Variables

> Create a .env file in your root directory with:

```dotenv
SECRET_KEY="..." # populate with appropriate secret
DEBUG=1
POSTGRES_HOST="db"
POSTGRES_PORT="5432"
POSTGRES_USER="works_user"
POSTGRES_DB="works"
POSTGRES_PASSWORD="..." # populate with appropriate secret
```

> *or load these env vars into your development environment*

#### 2- Build and Run the Application

```shell
docker compose up --build
```

> Ensure that database and application ports (5432, 8000) are free to use,
> or you can change it from the environment variables and `docker-compose.yml` file.

#### 3- Perform database migrations

```shell
docker compose exec web python manage.py migrate
```

#### 4- Visit http://127.0.0.1:8000

> You will find upload form to upload as many metadata files as you want.

- Click `Choose File`
- Choose a valid json file that contains `title`, `contributors` and `iswc` columns in
  any order.
- Confirm your selection by clicking `Open` or `Select` depending on you OS.
- Click `POST`

> You should have a response like this:

```json
{
  "file": "your_filename_and_maybe_some_other_chars.csv"
}
```

#### 5- Process uploaded files

```shell
docker compose exec web python manage.py ingest
```

> You should be getting similar output

```shell
Processing input files for reconciliation.
Parsing: #1-your_filename_and_maybe_some_other_chars.csv.
Parsing: #1-your_filename_and_maybe_some_other_chars.csv completed successfully.

```

#### 6- Validate through Django admin

> You can check all files and processed data on the admin page

- Create admin page user with `admin/admin` credentials

```shell
docker compose exec web python manage.py create_admin
```

- Visit http://127.0.0.1:8000/admin
- Enter username: `admin`, password: `admin` and hit login
- You can file the uploaded files
  here http://127.0.0.1:8000/admin/core/musicalworkmetadatafile/
- And the processed data here: http://127.0.0.1:8000/admin/core/musicalwork/

#### 7- Works by ISWC

> You can query a work by its ISWC, visit or cURL http://127.0.0.1:8000/?iswc=iswc_value

> You should be getting valid data if `iswc_value` is valid for any work

```shell
{
    "data": {
        "iswc": "T0101974597",
        "title": "Adventure of a Lifetime",
        "contributors": [
            "Selway Philip James",
            "O Brien Edward John",
            "Greenwood Colin Charles",
            "Yorke Thomas Edward"
        ]
    }
}
```


## Questions
#### 1- *Describe briefly the matching and reconciling method chosen*
- Try to retrieve the work by its iswc from the database ...
- If it's not found, try by its title and any of its contributors ...
- If it's not found, so it's considered a new work and shall be stored...
- Finally, if it's not newly created try to update the old missing data if exists.
- Contributors are cleaned between the new and the old data if exists.


#### 2- *We constantly receive metadata from our providers, how would you automatize the process?*
- Management command (ingest) should be automatically triggered by a cron-job or specialized workers if the server can handle it immediately.

#### 3- *Imagine that the Single View has 20 million musical works, do you think your solution would have a similar response time?*
- No.

#### 4- *If not, what would you do to improve it?*
- Data should be cleaned using one of the performant data processing tools pandas, numpy, etc.
to reduce database calls and queries as much as possible because im my solution for each row 
we execute about 4 database queries which is a lot for large datasets.
- Works should be sectioned as much as possible to reduce database load at each file processing. 
These sections can be by geographical location, provider, release dates, language, etc.