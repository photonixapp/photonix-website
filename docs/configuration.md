# Configuration

## Image analysis

In the user interface you can enable and disable individual types of image analysis (ML/AI). If you want to limit the CPU and RAM resources taken up by image analysis you can switch off the most intensive ones or just ones you are not interested in.

You can turn these on or off at any time. Newly imported photos still get queued up when turned off so will be analysed when/if you turn it back on.

### Benchmarks

Here are some benchmarks to help determine impact of each type of analysis. These are average times measured on a Raspberry Pi 4 for a single photo, single worker.

| Analysis | Average time (seconds) |
| -------- | ---------------------: |
| Color    |                  2.083 |
| Style    |                  2.240 |
| Location |                  3.707 |
| Face     |                 47.464 |
| Object   |                 52.796 |

## Environment variables

Docker containers are commonly configured to run via envirnment varables. You will see some default values that can be edited in your `docker-compose.yml` file. Here are details of what they mean.

| Variable Name       | Values        | Default    | Description  |
| ------------------- | ------------- | ---------- | ------------ |
| `ENV`               | `dev`, `prd`  |            | In `prd` mode, running code and services are as optimised as possible. Running in `dev` mode enables features like Webpack/React hot module reloading (HMR), Django Runserver (code auto-reloading), Storybook server etc. |
| `DEMO`              | `0`, `1`      | `0`        | Starts the environment with a demo user account, library and downloads some demo photos. This is how the demo at https://demo.photonix.org/ runs. You are restricted from performing certain data-modifying actions. |
| `SAMPLE_DATA`       | `0`, `1`      | `0`        | Creates same account, library and photos as in `DEMO` mode but still allows you to make modifying changes as a user (most useful for developers). |
| `POSTGRES_HOST`     | String        | `postgres` | Host name for Postgres database instance. |
| `POSTGRES_DB`       | String        | `photonix` | Database name for Postgres database instance, will be auto-created on first run if it doesn't exist. |
| `POSTGRES_USER`     | String        | `postgres` | Username for Postgres database. |
| `POSTGRES_PASSWORD` | String        | `postgres` | Password for Postgres database. |
| `POSTGRES_PORT`     | Integer       | `5432`     | Port for Postgres database. |
| `REDIS_HOST`        | String        | `redis`    | Redis hostname, used for resource locking. |
| `REDIS_PORT`        | Integer       | `6379`     | Redis port number. |
| `REDIS_DB`          | Integer       | `0`        | Redis database number. |
| `ALLOWED_HOSTS`     | String        | `*`        | Restricts access for Django backend to be accessed from just a certain hostname. |
| `ADMIN_USERNAME`    | String        |            | Creates a username for the admin user on first run. |
| `ADMIN_PASSWORD`    | String        |            | Sets password for the admin user on first run. If this is set but `ADMIN_USERNAME` is not, the username will be `admin`. |
| `DJANGO_SECRET_KEY` | String        | random     | Sets value for Django to use as a [secret key](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY) (sessions, hashing, signing etc.). By default we automatically generate a cryptographically secure key on first run and store it in Redis for future. |
| `LOG_LEVEL`         | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO`     | Determines what level of logging to output to terminal. |
| `DJANGO_LOG_LEVEL`  | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `WARNING`  | Determines what level of Django logging to output to terminal. |
