FROM tiangolo/uwsgi-nginx-flask:python3.6

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
ENV STATIC_INDEX 1
ENV UWSGI_INI /app/uwsgi.ini

COPY ./gemsearch /app/gemsearch
COPY ./static /app/static
COPY ./uwsgi.ini /app/uwsgi.ini
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt

