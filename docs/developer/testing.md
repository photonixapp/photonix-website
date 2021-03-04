# Testing

We have Python tests to cover most of the the server-side logic. We use pytest as a test runner and recommend running the tests inside the Docker container.

If you have the code checked out and can run Makefiles then you can start the container if it isn't already running:

    make start

If you can't run the Makefile directly (e.g. if you're on Windows) then you can see what the equivalent command would be by looking inside that file. The command for starting the environment with out make is:

    docker-compose -f docker/docker-compose.dev.yml up

In another teminal connect to the Photonix Docker container and execute the test runner:

    make shell
    python test.py

To start the shell without make would be:

    docker-compose -f docker/docker-compose.dev.yml exec photonix bash

If you are only interested in a particular test and want to save time you can add the test file path as an extra argument, i.e:

    python test.py tests/test_metadata.py

If you are familiar with pytest then you can add extra arguments to the end and they will be passed through.

If you are an expert with pytest and have suggestions for improving this setup then please do get in touch with your suggestions.
