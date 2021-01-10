# Configuration

## Environment variables

Docker containers are commonly configured to run via envirnment varables. You will see some default values that can be edited in your `docker-compose.yml` file. Here are details of what they mean.

| Variable Name       | Values        | Default    | Description  |
| ------------------- | ------------- | ---------- | ------------ |
| `ENV`               | `dev`, `prd`  |            | In `prd` mode, running code and services are as optimised as possible. Running in `dev` mode enables features like Webpack/React hot module reloading (HMR), Django Runserver (code auto-reloading), Storybook server etc. |
| `DEMO`              | `0`, `1`      | `0`        | Starts the environment with a demo user account, library and downloads some demo photos. This is how the demo at https://demo.photonix.org/ runs. |
| `POSTGRES_HOST`     | String        | `postgres` | Host name for Postgres database instance. |
| `POSTGRES_DB`       | String        | `photonix` | Database name for Postgres database instance, will be auto-created on first run if it doesn't exist. |
| `POSTGRES_USER`     | String        | `postgres` | Username for Postgres database. |
| `POSTGRES_PASSWORD` | String        | `postgres` | Password for Postgres database. |
| `REDIS_HOST`        | String        | `redis`    | Redis hostname, used for resource locking. |
| `ALLOWED_HOSTS`     | String        | `*`        | Restricts access for Django backend to be accessed from just a certain hostname. |
| `ADMIN_USERNAME`    | String        |            | Creates a username for the admin user on first run. |
| `ADMIN_PASSWORD`    | String        |            | Sets password for the admin user on first run. If this is set but `ADMIN_USERNAME` is not, the username will be `admin`. |
