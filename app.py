from sanic import Sanic
from sanic_motor import BaseModel
from sanic_redis import SanicRedis

app = Sanic('myapp')

settings = {
    'MOTOR_URI': 'mongodb://localhost:27017/myapp',
    'REDIS': {'address': ('127.0.0.1', 6379), }
}
app.config.update(settings)

BaseModel.init_app(app)
redis = SanicRedis(app)
