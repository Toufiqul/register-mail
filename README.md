This project has one API endpoint at "/register".
This endpoint takes the user's email address and saves it to a database, returns a JSON response and sends the user a confirmation email.

Tech stack:

- Flask
- SQLite
- SQLAlchemy
- Gmail API

#### to run

- clone the repository https://github.com/Toufiqul/register-mail.git
- build docker image

```
docker build -t register-mail .
```

- run docker container

```
docker run -p 5000:5000 -w /app -v "$(pwd):/app" register-mail

```

var.py file at "resources/var.py"
