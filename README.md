# WoI - Words Of Interest

Simple blog engine written in Python and Django.

## Local usage

It is recommended to run WoI in a virtual environment. WoI uses
[Poetry](https://python-poetry.org) for dependency management, so it must
be installed first. During the woi_run_first command you will be prompted
to create a superuser and asked for some basic configuration values for
your blog. Many more settings can be tweaked in the settings.py file.

```
$ python -m venv woi-env
$ cd woi-env/
$ source bin/activate
$ pip install -U pip
$ pip install poetry
$ git clone https://github.com/whitie/WordsOfInterest.git
$ cd WordsOfInterest/
$ poetry install
$ cd woi/
$ python manage.py woi_run_first --readme
$ python manage.py runserver
```

If everything went without errors, point your Browser to http://localhost:8000.
