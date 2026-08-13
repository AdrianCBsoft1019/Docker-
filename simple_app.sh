#!/bin/bash

mkdir tempdir
mkdir tempdir/templates
mkdir tempdir/static

cp simple_app.py tempdir/.
cp -r templates/* tempdir/templates/.
cp -r static/* tempdir/static/.

echo "FROM python" >> tempdir/Dockerfile
echo "RUN pip install flask" >> tempdir/Dockerfile
echo "COPY ./static /home/turus/proyecto/roderick/static/" >> tempdir/Dockerfile
echo "COPY ./templates /home/turus/proyecto/roderick/templates/" >> tempdir/Dockerfile
echo "COPY ./simple_app.py /home/turus/proyecto/roderick/" >> tempdir/Dockerfile

echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python3 /home/turus/proyecto/roderick/simple_app.py" >> tempdir/Dockerfile