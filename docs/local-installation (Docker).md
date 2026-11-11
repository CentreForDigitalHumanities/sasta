# Before you start

Running the containerized version of SASTA bypasses the need to install system dependencies.

You need to install the following software:

-   [Docker](https://docs.docker.com/get-docker/). Make sure Docker has at least 4GB memory allocated.

# Running locally

To download, build, install, and run all containers:

```console
docker compose up
```

If everything is executed correctly, the application can be opened at [localhost:80](localhost:80).

# First-use setup

## Create an admin account

Create a superuser using the Django command in the running backend container.
Choose a username, email and password. Email does not have to be real (but cannot be blank):

```console
docker compose exec backend python manage.py createsuperuser
```

The email address of a superuser is verified automatically, so you can log in to the application with this account right away.

## Add SASTADEV method definitions

The method definition spreadsheets are part of the [sastadev][sd-link] package, in its `data/methods` directory. Copy them to a convenient location, then upload:

1. Go to [localhost:80/admin](http://localhost:80/admin)
2. Log in with your admin account
3. `analysis` -> `Assessment methods` -> `Add new`
4. Choose the following settings:
    - Category: `TARSP`
    - File: `TARSP_Index_Current.xlsx` (xlsx spreadsheet)
5. Repeat step 3 & 4 for STAP and ASTA

[sd-link]: https://github.com/CentreForDigitalHumanities/sastadev/
