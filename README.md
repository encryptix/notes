
notes
=====

Python based webapp for storing notes
Repo is split into frontend and backend parts

Example deployment
=====
Frontend code is placed in /var/www/notes/ and a config file is created as
/etc/nginx/sites-available/notes. This is then symlinked to /etc/nginx/sites-enabled/

Example Conf: 

    server {

        listen   80; ## listen for ipv4; this line is default and implied

        root /var/www/notes/;
        index index.html index.htm;

        server_name notes.example.com www.notes.example.com;

        try_files $uri $uri/ /404.html;

        location /interface.wsgi{
                include uwsgi_params;
                uwsgi_pass 127.0.0.1:30001;
        }
        error_page 404 /404.html;
    }


The backend code is then placed in /var/apps/notes/ and a config file created at
/etc/uwsgi/apps-available/notes.ini. This is then symlinked to /etc/uwsgi/apps-enabled/

Example Conf:

    [uwsgi]
    master = true
    chdir = /var/apps/notes/
    module = interface
    processes = 1
    max-requests = 1000
    plugins = python
    socket = 127.0.0.1:30001
    chmod-socket = 777
    logto = /var/log/uwsgi/app/notes.log
    logfile-chown = www-data


uwsgi and nginx are then restarted:

    sudo service uwsgi restart
    sudo service nginx restart


