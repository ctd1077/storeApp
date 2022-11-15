FROM python:3.7.0
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# CMD [“flask”, “run”, “--host”, “0.0.0.0”]
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD ["flask", "run", "--host=0.0.0.0"]