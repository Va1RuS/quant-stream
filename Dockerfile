FROM python:3.10-slim

WORKDIR /usr/src/quant-stream

COPY . .

RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY entrypoint.sh /usr/src/quant-stream
RUN chmod +x /usr/src/quant-stream/entrypoint.sh


ENV PYTHONPATH=/usr/src/quant-stream

CMD ["/usr/src/quant-stream/entrypoint.sh"]