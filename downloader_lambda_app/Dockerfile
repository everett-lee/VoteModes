FROM public.ecr.aws/lambda/python:3.8

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY __init__.py ./
COPY downloader_lambda.py ./
COPY request_executors/ ./

CMD ["downloader_lambda.handler"]