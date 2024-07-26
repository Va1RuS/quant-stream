FROM python:3.10-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

COPY entrypoint.sh /usr/src/app
RUN chmod +x /usr/src/app/entrypoint.sh

CMD ["/usr/src/app/entrypoint.sh"]