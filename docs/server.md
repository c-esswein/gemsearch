

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
sudo systemctl restart gemsearch
sudo chown -R nginx:nginx .
sudo chcon -t httpd_sys_rw_content_t /var/www/gemsearch_api/gemsearch.sock



## MongoDb

Required indexes for performance:
- tracks: uri
- artists: uri
- users: userName

Example: db.tracks.createIndex( { "uri": 1 } )