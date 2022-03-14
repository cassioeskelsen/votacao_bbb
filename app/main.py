from random import randrange

from sanic import Sanic, response, text
from sanic_redis import SanicRedis
import json

redis_server = "20.226.17.17"

app = Sanic("Example")
app.config.update(
    {
        'REDIS': f"redis://{redis_server}/0"
    }
)
redis = SanicRedis()
redis.init_app(app)


@app.route("/vote", methods=['POST'])
async def vote(request):
    choice = randrange(3)
    async with redis.conn as conn:
        await conn.rpush("votos", json.dumps(
            {"ip": request.ip, "user-agent": request.headers['user-agent'], "body": f"choice={choice}"}))

    return response.json(
        {'message': 'Voto Recebido'},
        status=202
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False, access_log=False, workers=10)
