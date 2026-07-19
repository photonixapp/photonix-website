# Configuration

## Image analysis

In the user interface you can enable and disable individual types of image analysis (ML/AI). If you want to limit the CPU and RAM resources taken up by image analysis you can switch off the most intensive ones or just ones you are not interested in.

You can turn these on or off at any time. Newly imported photos still get queued up when turned off so will be analysed when/if you turn it back on.

Semantic search ("Natural language" search mode, powered by CLIP) is the one analysis type that is off by default — it involves the largest model download (~340 MB) so you opt in per library from Settings or during onboarding.

### Benchmarks

The 2026 migration to ONNX Runtime made analysis dramatically cheaper than earlier releases. Average per-photo times on an 8-core x86 desktop CPU (thread caps at their defaults), measured over a mixed set of 6-16 megapixel photos:

| Analysis | Average time (seconds) | Peak process RAM |
| -------- | ---------------------: | ---------------: |
| Color    |                   0.08 |           205 MB |
| Style    |                   0.05 |           295 MB |
| Location |                 < 0.01 |            ~50 MB |
| Face     |                   0.08 |           325 MB |
| Object   |                   0.07 |           399 MB |
| Semantic (CLIP) |            0.02 |           350 MB |

For comparison, the TensorFlow stack these replaced needed several seconds per photo for object and face analysis (75× and 26× slower respectively) and up to 4 GB of RAM for the object detector. Raspberry Pi timings will be proportionally slower than the desktop numbers above but benefit from the same speedups.

If image analysis is still too heavy for the machine serving your photos, it can be moved wholly into a separate `photonix-ml` container, optionally on a different machine — see [Installing](installing.md).

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
| `REDIS_PASSWORD`    | String        |            | Redis password (not used by default). |
| `ALLOWED_HOSTS`     | String        | `*`        | Restricts access for Django backend to be accessed from just a certain hostname. |
| `ADMIN_USERNAME`    | String        |            | Creates a username for the admin user on first run. |
| `ADMIN_PASSWORD`    | String        |            | Sets password for the admin user on first run. If this is set but `ADMIN_USERNAME` is not, the username will be `admin`. |
| `DJANGO_SECRET_KEY` | String        | random     | Sets value for Django to use as a [secret key](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY) (sessions, hashing, signing etc.). By default we automatically generate a cryptographically secure key on first run and store it in Redis for future. |
| `LOG_LEVEL`         | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `INFO`     | Determines what level of logging to output to terminal. |
| `DJANGO_LOG_LEVEL`  | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` | `WARNING`  | Determines what level of Django logging to output to terminal. |
| `CLASSIFICATION_DISABLED` | `0`, `1` | `0`   | When `1`, this container runs no image-analysis workers — for deployments running classification in a separate `photonix-ml` container (see [Installing](installing.md)). |
| `CLASSIFIER_MAX_INFERENCE_SIZE` | Integer | `1024` | Longest edge (pixels) images are downscaled to before object/face analysis. `0` runs on full-resolution originals (much slower, rarely better). |
| `CLASSIFIER_INTRA_OP_THREADS` | Integer | `2`  | CPU threads each analysis model may use for a single operation. Keeps the six analysis workers from saturating every core; `0` leaves the runtime default. |
| `CLASSIFIER_INTER_OP_THREADS` | Integer | `2`  | CPU threads each analysis model may use across independent operations. `0` leaves the runtime default. |
| `CLASSIFIER_IDLE_TIMEOUT` | Integer (seconds) | `300` | How long an analysis model stays loaded in memory after its last use before being unloaded. |
| `CLASSIFIER_MEMORY_BUFFER_MB` | Integer | `500` | Free-memory safety buffer that must remain available before an analysis model is allowed to load. |
