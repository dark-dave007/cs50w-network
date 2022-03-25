# Network

This project was inspired by [CS50 Web Programming with Python and JavaScript](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/).

[Full project specification](https://cs50.harvard.edu/web/2020/projects/4/network/).

## Setup

The first thing to do is clone this repository:

```bash
git clone https://github.com/dark-dave007/cs50w-network
cd cs50w-network
```

Install dependencies:

```bash
python3 -m pip install Django
```

Migrate:

```bash
python3 manage.py makemigrations network
python3 manage.py migrate network
```

To run the development server:

```bash
python3 manage.py runserver
```

If you would like to create an admin user, run the following:

```bash
python3 manage.py createsuperuser
```

And follow the instructions given by Django.

### Details

The project I made is a social network, similar to twitter that will allow users to make posts, like, and follow users.

This project was made using [Django](https://www.djangoproject.com/) and [Bulma](https://bulma.io).
