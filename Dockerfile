FROM grahamdumpleton/mod-wsgi-docker:python-3.5-onbuild
CMD [ "gemsearch.wsgi" ]