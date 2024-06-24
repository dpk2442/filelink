# FileLink

A simple app to generate public links to files. Simply point the service at a directory of files,
and after logging in to the UI download links can be created for any file in that directory.

## Deploying

### Option 1: Use the pre-built docker container

Releases of FileLink are automatically built into a container available at `ghcr.io/dpk2442/filelink`.
In the simplest form, the service can be run as follows:
```
docker run \
    --volume <Path to store application data>:/app/data \
    --volume <Path to files to serve>:/files \
    --publish-all \
    ghcr.io/dpk2442/filelink
```

#### Volumes
The container needs two volumes mounted to properly function.
| Container Path | Description |
| -------------- | - |
| /app/data      | Directory where the application database and secret key are stored. |
| /files         | Directory that will be available in the application to create shares from.  |

### Option 2: Directly deploy the service

This is the more advanced option, and requires some manual setup. The application should be run using
the `filelink.settings.prod` settings, and the `requirements.txt` should have all the dependencies
needed to run the application, including uwsgi if desired. See the `run.sh` script for a reference of
what commands need to be run to bootstrap the system.

The `FL_FILES_PATH` environment variable can be set to override the default files path of `/files`. If
using `uwsgi.ini` with a non-standard path, be sure to update the `static-safe` parameter.

See
[How to deploy Django](https://docs.djangoproject.com/en/5.0/howto/deployment/) for more information
about deploying Django applications.

## Development

### Option 1: Use VSCode

Prequisites:
- [VSCode](https://code.visualstudio.com/)
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

Clone the project and open it in the container. All of the needed extensions and python dependencies should be
automatically installed. Once it finishes, open the shell and run the following commands:

```
mkdir data
python manage.py migrate
python manage.py generate_secret_key
python manage.py runserver
```

### Option 2: Use python directly

Prequisites:
- [Python 3.12](https://www.python.org/downloads/release/python-3124/)

Clone the project, navigate into it in the terminal, and run the following commands:

```
python -m pip install -r requirements_dev.txt
mkdir data
python manage.py migrate
python manage.py generate_secret_key
python manage.py runserver
```

### Create a new migration

After making updates to the model classes, create a migration using the following command:

```
python manage.py makemigrations shares
```

### Running tests

Tests can be run using `pytest` or Django's built in test runner:
```
python manage.py test
pytest
```
