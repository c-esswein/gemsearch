# Server Overview 

## Webserver-Files
located at `/var/www/`

## Ngnix
config is stored at:  `/etc/nginx/conf.d/gemsearch.conf`


## uwsgi
service is configured at: `/etc/systemd/system/gemsearch.service `

To restart the gemsearch api (e.g. for replacing code or the embedding) run:
`sudo systemctl restart gemsearch`


If you have troubles with the permissions, set context for socket file:
`sudo chcon -t httpd_sys_rw_content_t /var/www/gemsearch_api/gemsearch.sock`


## Deployment:
```
cd /var/www/gemsearch_api
git pull
sudo systemctl restart gemsearch
sudo chcon -t httpd_sys_rw_content_t /var/www/gemsearch_api/gemsearch.sock




sudo systemctl restart nginx

sudo chown -R christian:nginx .
```

## Logs:

`/var/log/uwsgi/%n.log`

and

`/var/log/nginx/%n.log`

## MongoDb

Required indexes for performance:
- tracks: uri
- artists: uri
- users: userName

Example: `db.tracks.createIndex( { "uri": 1 } )`


## Services

The api needs two additional services:

### Crawler
Watches for new tracks and crawls tag and artist data.

```
python3 -m gemsearch.services.crawler
```

Crawled tracks are transitioned to: `track['gemsearch_status'] = 'CRAWLED'`

### Embedder
Watches for new users (after all tracks are crawled) and creates new embedding

```
python3 -m gemsearch.services.new_user_watcher
```

Users are transitioned to: `user['userStatus'] = 'EMBEDDED'`
