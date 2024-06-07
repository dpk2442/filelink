# FileLink

A simple app to generate public links to files.

## Development

### Option 1: Use VSCode

Prequisites:
- [VSCode](https://code.visualstudio.com/)
- [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

Clone the project and open it in the container. All of the needed extensions and python dependencies should be
automatically installed. Once it finishes, open the shell and run the following commands:

```
python manage.py migrate
python manage.py runserver
```

### Option 2: Use python directly

Prequisites:
- [Python 3.12](https://www.python.org/downloads/release/python-3124/)

Clone the project, navigate into it in the terminal, and run the following commands:

```
python -m pip install -r requirements_dev.txt
python manage.py migrate
python manage.py runserver
```

### Create a new migration

After making updates to the model classes, create a migration using the following command:

```
python manage.py makemigrations shares
```

### Running tests

```
python manage.py test shares
```
