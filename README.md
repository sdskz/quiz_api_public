# Install
App can only run locally in debug mode.
Source code includes vast comments and each step description

Django 3.2.11

- `pip install -r requirements.txt`
- superuser credentials login: `admin`, password: `admin`
- postgres is NOT implemented (only sqlite for easy installation)
- `/admin/` panel is implemented
- `/swagger/` is implemented
- admin has privileges to change/delete any values in database via admin panel
- user can only retrieve data via API
- only `POST` and `GET` requests are implemented (server will not respond if user send any other request)
- complicated data validation is not supported
- full endpoints description via url `/swagger/`

