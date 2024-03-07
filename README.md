This project has one API endpoint at "/register".
This endpoint takes the user's email address and saves it to a database, returns a JSON response and sends the user a confirmation email.

Tech stack:

- Flask
- SQLite
- SQLAlchemy
- Gmail API
- Gunicorn server for deployment

#### to run



- clone the repository https://github.com/Toufiqul/register-mail.git
- add gmail api credentials in resources/credentials.json
- build docker image

```
docker-compose up --build
```
