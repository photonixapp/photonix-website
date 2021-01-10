# Adding or upgrading JavaScript packages with Yarn

Make sure you are running the development Docker container and have a shell open

    make start
    make shell  # New terminal

Change into the `ui` directory and use `yarn` to add packages.

    cd ui
    yarn add PACKAGENAME

Confirm `ui/yarn.lock` has changes:

    git diff ui/yarn.lock

Confirm dev Docker image still builds and runs:

    make build && make start
