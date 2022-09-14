FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE $PORT
# CMD python main.py 
CMD gunicorn -w 4 -b 0.0.0.0:$PORT main:app