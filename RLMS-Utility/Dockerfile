# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.6
USER root 

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

# Install required language models
RUN python -m nltk.downloader "punkt"
RUN python -m nltk.downloader "wordnet" 

WORKDIR /app
ADD . /app

# During debugging, this entry point will be overridden. For more information, refer to https://aka.ms/vscode-docker-python-debug
ENTRYPOINT python app.py
