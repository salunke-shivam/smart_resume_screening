FROM python:3.11-slim

WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project code
COPY . .

# expose port for api
EXPOSE 8000

# run the server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]