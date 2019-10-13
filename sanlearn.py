from sanic import Sanic
from sanic.response import json
from sanic_motor import BaseModel

app = Sanic('myapp')

settings = {
    'MOTOR_URI': 'mongodb://localhost:27017/myapp'
}
app.config.update(settings)
BaseModel.init_app(app)


class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['first_name', 'last_name']

    def __repr__(self):
        return str({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age
        })


@app.route("/users", methods=['GET', 'POST'])
async def test(request):
    if request.method == 'POST':
        first_name = request.json.get('first_name', '').strip().lower()
        last_name = request.json.get('last_name', '').strip().lower()
        age = request.json.get('age', '')
        if first_name and last_name:
            is_uniq = await User.is_unique(doc=dict(first_name=first_name, last_name=last_name))
            if is_uniq in (True, None):
                await User.insert_one(dict(first_name=first_name, last_name=last_name, age=int(age)))
                return json({"result_code": "0", "result_message": "User was added successfully."})
            else:
                return json({"result_code": "-1", "result_message": "User already exists."})
        else:
            return json({"result_code": "-2", "result_message": "first_name and last_name cannot be empty"})
    else:
        cur = await User.find()
        return json({"users": str(cur.objects)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
