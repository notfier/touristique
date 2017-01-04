# Touristique backend API

Simple touristic backend API.


### Setup

First you must have installed Python 2.7, pip, virtualenv.
Under virtualenv run next command:

```
pip install -r requirements.txt
```

Run following commands to setup project:

```
./manage.py makemigrations
./manage.py migrate
./manage.py loaddata fixtures.json
```

To run server:

```
./manage.py runserver
```

To run tests:

```
./manage.py test
```

To look through Touristique API:

```
localhost:8000/api/docs/
```

### Usage

You can test API on Touristique client side (run client side and check localhost:3000) providing following credentials:

Field                | Value
---------------------|------------------------------------------------------
`username`           | `admin@admin.com`
`password`           | `admin12345`

Now you are an operator and you can edit/add a tourist providing card id (for instance, 1fdd8cbb9e3a48779f4296007333bb0f or any of fixtures touristcard pk as a card id number).
Also as administrator you can add new operators in django admin ('/api/admin/') in 'Users' section and add/edit/remove operators(users) whatever you want or need. So, operators(users) manipulate over any tourist's info and department location.
