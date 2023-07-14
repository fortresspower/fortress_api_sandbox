# Build: docker build -t gridfabric:python-middleware .
# Run: docker run --name=pythonmiddleware -it --rm --network=gridfabric gridfabric:python-middleware

FROM python:3.11-slim

WORKDIR /src

COPY ./src /src/
RUN pip install -r requirements.txt

EXPOSE 8081
ENTRYPOINT [ "python", "middleware.py" ]
