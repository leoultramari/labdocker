# Importando o módulo do Flask e o módulo os
from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'), db=0, socket_connect_timeout=2, socket_timeout=2)

# Objeto da Classe Flask que vamos usar para configurar e executar a aplicação
app = Flask(__name__)

# Definindo a rota padrão da aplicação.
@app.route("/")

# Função que tem como objetivo printar uma mensagem já em formato HTML na tela.
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    html =	"<h3>Hostname: {hostname}</h3>" \
    		"<h3>Message: {message}</h3>" \
        	"<b>Visits:</b> {visits}"
    return html.format(message=os.getenv("MESSAGE", "Hello world"), visits=visits, hostname=socket.gethostname())

# Garantindo que o módulo não será executado se ele for importado por outro módulo.
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)