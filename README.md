# github-monitor

Github commits monitor

## Execution instructions

First, copy the sample .env file.

`$ cp .env.sample .env`

Then edit the file setting appropriate values for all the configs, preferably with long, random values.

Remember to fill `DATABASE_URL` with the correct values provided in `POSTGRES_*` variables.

You can generate the github keys for `SOCIAL_AUTH_*` at: https://github.com/settings/applications/new
- When generating the keys, use `http://localhost:8000/oauth/complete/github/` as the callback URL

For the execution of this project, you'll need docker and docker installed. Check the instructions for their installations in all operating systems:

Docker: https://docs.docker.com/get-docker/

Docker-compose: https://docs.docker.com/compose/install/

After the installation of the above tools and with the right values in .env, you should be able to run the project with:

`$ docker-compose up -d`

This will build and run all the required services for this application to run.
If everything ran sucessfully, you should be able to visit the application at http://localhost:8000
- Make sure that you're using `http://` and not `https://`, as the browser may sometimes add `https://` if you don't specify it

To execute commands such as migrations, run:

`$ docker-compose run api python manage.py migrate`

To check the logs for:
- Django application, run: `docker-compose logs -f api`.
- Webpack, run: `docker-compose logs -f webpack`.
