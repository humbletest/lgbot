# Minimal Python / Flask server for Heroku

Provides a minimal setup that runs as a Python / Flask server both locally and on Heroku.

# Installation

Create an environment with `pipenv`, then run

```Python
pipenv install
```

For development open a pipenv shell:

```Python
pipenv shell
```

or run commands in the `env` with:

```Python
pipenv run [command arg1 arg2 ...]
```

# Start server locally

To start the server locally use:

```Python
python start_server_locally.py
```

Under Windows use `s.bat` to start a local server or `f.bat` to start a development server.

In the browser navigate to `localhost:5000`.

## Note

All files with `.bat` extension are convenience for Windows development. You can delete them without any loss of server functionality.

`p.bat [commit name]` can be used to push changes to Heroku ( example: `p Initial commit` )

`r.bat [command arg1 arg2 ...]` can be used to run a command with args in the `env` ( example: `r f` starts development server in `env`)
