FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install flask
RUN pip install gunicorn
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["gunicorn", "--bind","0.0.0.0:5000","app:create_app()"]