uwsgi --socket 0.0.0.0:443 --enable-threads --protocol=http -w wsgi:app
