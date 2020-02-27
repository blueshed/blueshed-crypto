"""
    from https://devcenter.heroku.com/articles/container-registry-and-runtime
"""
from invoke import task
from cryptography.fernet import Fernet
from web.main_handler import MainHandler


@task
def gen_key(_, path="key.key"):
    """ generates a key file """
    key = Fernet.generate_key()
    with open(path, "wb") as file:
        file.write(key)  # The key is type bytes still


@task
def encrypt(_, message):
    """ encrypts message with key file """
    print(MainHandler.encrypt(message))


@task
def decrypt(_, message):
    """ decrypts message with key file """
    print(MainHandler.decrypt(message))


@task
def release(ctx):
    """ release to heroku (heroku container:login)"""
    ctx.run("heroku container:push web -a blueshed-crypto")
    ctx.run("heroku container:release web -a blueshed-crypto")
    # ctx.run("heroku open -a blueshed-crypto")
