FROM python:3.8.16

WORKDIR /app/

COPY requirements.txt /app/

RUN pip3 install -r requirements.txt

COPY . /app/

EXPOSE 8080

CMD python app.py -port=8080 ${DEMO_VERSION:+-version=$DEMO_VERSION} ${DEMO_COLOR:+-color=$DEMO_COLOR}


# docker build -t harbor.cloud.netease.com/qztest/nsm-python-demo:v4.2.1 .
# docker push harbor.cloud.netease.com/qztest/nsm-python-demo:v4.2.1

