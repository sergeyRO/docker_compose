FROM python:3.9.6-alpine
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN mkdir -p /app
RUN mkdir -p /app/staticfiles
RUN mkdir -p /app/stocks_products/stocks_products
RUN mkdir -p /app/stocks_products/logistic
ADD ./* /app
ADD ./stocks_products/stocks_products /app/stocks_products/stocks_products
ADD ./stocks_products/logistic /app/stocks_products/logistic
RUN ls -lrt /app
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
EXPOSE 8000


