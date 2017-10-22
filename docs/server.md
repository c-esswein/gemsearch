

## Files
at /var/www/

## Ngnix
config at:  /etc/nginx/conf.d/gemsearch.conf


## uwsgi
service at: /etc/systemd/system/gemsearch.service 

sudo systemctl restart gemsearch


set context for socket file:
sudo chcon -t httpd_sys_rw_content_t /var/www/gemsearch_api/gemsearch.sock


## Deployment:
cd /var/www/gemsearch_api
git pull
sudo systemctl restart gemsearch
sudo chcon -t httpd_sys_rw_content_t /var/www/gemsearch_api/gemsearch.sock




sudo systemctl restart nginx

sudo chown -R christian:nginx .

## Logs:

/var/log/uwsgi/%n.log
and
/var/log/uwsgi/%n.log

## MongoDb

Required indexes for performance:
- tracks: uri
- artists: uri
- users: userName

Example: db.tracks.createIndex( { "uri": 1 } )