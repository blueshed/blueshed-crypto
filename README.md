# blueshed-crypto #

This project is a web service to encrypt and decrypt simple text messages.

It is actually an exploration of developing in containers rather than a virtual environment.

### Local ###
To run the development environment you just:

```
docker-compose up
```

If you change the environment you will need to stop the container and run:

```
docker-compose build
```

before calling up again.

That will build and run the container locally. The local directory is mounted and tornado performs a hot-reload on the files.

### Deploy ###

To deploy with heroku you would:

```
heroku container:login
heroku create
heroku container:push web
heroku container:release web
heroku open
```

This will create an app that you can rename later.

#### References: ####

https://devcenter.heroku.com/articles/container-registry-and-runtime
