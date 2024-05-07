"""
    from https://devcenter.heroku.com/articles/container-registry-and-runtime
"""
from invoke.tasks import task
from cryptography.fernet import Fernet
from blueshed.crypto import api

@task
def run(ctx, debug=False):
    """ run our server """
    ctx.run(f'python3 -m blueshed.crypto.main{" --debug" if debug else ""}', pty=True)


@task
def gen_key(_, path="key.key"):
    """ generates a key file """
    key = Fernet.generate_key()
    with open(path, "wb") as file:
        file.write(key)  # The key is type bytes still


@task
def encrypt(_, message):
    """ encrypts message with key file """
    print(api.encrypt(message))


@task
def decrypt(_, message):
    """ decrypts message with key file """
    print(api.decrypt(message))


@task
def lint(ctx):
    """format and check"""
    ctx.run('ruff format', pty=True)
    ctx.run('ruff check --select I --fix', pty=True)


@task
def release(ctx):
    """ release to heroku (heroku container:login)"""
    ctx.run("heroku container:push web -a blueshed-crypto")
    ctx.run("heroku container:release web -a blueshed-crypto")
    ctx.run("heroku open -a blueshed-crypto")
