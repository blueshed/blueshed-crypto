FROM python:3.9-slim
RUN apt-get update && apt-get install -y git

ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/webapp/
WORKDIR /opt/webapp

# Expose is NOT supported by Heroku
# EXPOSE 8080
ENV PYTHONPATH ".:${PYTHONPATH}"

# Run the image as a non-root user
RUN useradd -m myuser
RUN chown myuser:myuser -R /opt/webapp/
USER myuser


# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
CMD python3 -m web.app
