# Base image for Python application
FROM python:3.12-alpine

# Create a working directory within the container
WORKDIR /app

# Copy requirements.txt file
COPY requirements.txt .

# Install dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY templates ./templates
COPY src ./src

ENV DATABASE_URL=mysql+pymysql://root:KddxbadXMHBPXXhCZzxznUdyeZsPUliu@viaduct.proxy.rlwy.net:33428/railway
ENV SECRET_KEY=8890ca4bc6440e29b91a23bdc55d72e39a79630ab0f11e71ead2cd5eaa2b262b
ENV ALGORITHM=HS256
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30
ENV MAIL_USERNAME=testapideveloper9@gmail.com
ENV MAIL_FROM=testapideveloper9@gmail.com
ENV MAIL_PASSWORD=wbdbyhxwyapjdcxd
ENV MAIL_PORT=587
ENV MAIL_SERVER=smtp.gmail.com

EXPOSE 8000

# Command to run the application (replace "main:app" with your actual entry point)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
