import os, json
from flask import Flask, render_template, request
from pymemcache.client.base import Client

app = Flask(__name__)
port = int(os.environ.get("PORT", 8000))


def json_serializer(key, value):
    if type(value) == str:
        return value, 1
    return json.dumps(value), 2


def json_deserializer(key, value, flags):
   if flags == 1:
       return value.decode("utf-8")
   if flags == 2:
       return json.loads(value.decode("utf-8"))
   raise Exception("Unknown serialization format")


client = Client((os.environ.get("CACHE"), 11211), serializer=json_serializer, deserializer=json_deserializer)


@app.route('/')
def index():
    number = request.args.get('number')
    result = "none"
    if number:
        cached = client.get(number)
        if cached:
            result = cached + " (cached result)"
        else:
            result = fibo(int(number))
            client.set(number, str(result))
    return render_template('index.html', answer=result)


def fibo(n):
    if n in [0,1]:
        return n
    else:
        return fibo(n-1) + fibo(n-2)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)