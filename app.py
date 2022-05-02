from flask import Flask, render_template, Response
from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient(hosts='192.168.178.31:9092')

app = Flask(__name__)

@app.route('/')
def index():
    return(render_template('index.html'))

#Consumer API
#Beispiel hier http://localhost:5001/topic/geodata_final123#
#Example: https://medium.com/code-zen/python-generator-and-html-server-sent-events-3cdf14140e56
# https://maxhalford.github.io/blog/flask-sse-no-deps/

@app.route('/topic/<topicname>')
def get_messages(topicname):
    client = get_kafka_client()
    def events():
        for i in client.topics[topicname].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return Response(events(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, port=5001)