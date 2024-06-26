FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV API_KEY=SUA_API_KEY

EXPOSE 5000

CMD ["python", "main.py"]