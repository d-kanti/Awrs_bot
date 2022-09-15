FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
# RUN python main.py
# EXPOSE $PORT4
CMD ["bash","start.sh"]
# CMD gunicorn --bind 0.0.0.0:$PORT webserver:app