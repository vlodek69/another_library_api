# Another Library API

Service for managing book records.

## Installation

Python3 must be already installed.

```shell
git clone https://github.com/vlodek69/another_library_api
cd another_library_api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
```
Copy .env-sample -> .env and populate with all required data.

Install requirements by running:
```shell
pip install -r requirements.txt
```

Run migrations
```shell
python manage.py migrate
```

To start the server simply do
```shell
python manage.py runserver
```

## How to use

Access browsable API at base url