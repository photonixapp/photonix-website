# Users and Libraries

Photonix supports multiple users and multiple libraries in a single installation. This is useful in use cases such as families and businesses. For example, all family members could have their own usernames and passwords to log in to Photonix and have therir own private libraries. An admin of the system could also set up a shared library which all other family members also have access to. Users can then switch between the library they wish to view by selecting it in their account menu.

The user interface for managing this is easily is yet to be developed but things can be configured on the command line if you wish to use Photonix in this way.

## Command line interface (CLI)

To run any of the following commands you will need to have Photonix currently running under Docker.

### Creating libraries

You will be propted to create a library when you first run Photonix.

To create an additional library and assign a user to it, run the following from the host machine where you have your `docker-compose.yml` file:

    docker-compose exec photonix ./manage.py create_library USERNAME "LIBRARY NAME"

### Creating users

You likely already created an admin user if you went through the onboarding process of a new installation already.

For each additional user you wish to add, run this from the host machine (where you have your `docker-compose.yml` file). You will also be asked whether you wish to add the new user to an existing library;

    docker-compose exec photonix ./manage.py create_user
