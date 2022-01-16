# WoI - Words Of Interest

Simple blog engine written in Python and Django. The database adapter defaults
to [SQLite](https://www.sqlite.org), but usage of
[PostgreSQL](https://www.postgresql.org/) and others are possible, see
[Django docs](https://docs.djangoproject.com/en/4.0/ref/databases/).

## Local usage (Linux/Unix)

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
To start WoI on every login, you can create a systemd user service:

```
# File: ~/.config/systemd/user/woi.service
[Unit]
Description=Run Words Of Interest on login

[Service]
Restart=on-failure
WorkingDirectory=<PATH_TO>/woi-env/WordsOfInterest/woi
ExecStart=<PATH_TO>/woi-env/bin/python <PATH_TO>/woi-env/WordsOfInterest/woi/manage.py runserver

[Install]
WantedBy=multi-user.target
```

After creation of the file run `systemctl --user enable woi.service --now`.
