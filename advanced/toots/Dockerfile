FROM python:3.7-slim

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./listen_local_updates.py .
COPY ./Mastodon.py /usr/local/lib/python3.7/site-packages/mastodon/Mastodon.py

ENV PYTHONUNBUFFERED true
# CMD [ "python", "-u", "./listen_local_updates.py" ]
CMD ["python", "listen_local_updates.py"]
