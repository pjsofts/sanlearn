from sanic.response import json

from app import app
from models.user import User
from results.results import Results
from utils.sanic_rate_limit import rate_limited


@app.route("/users", methods=['GET', 'POST'])
@rate_limited(10)
async def test(request):
    if request.method == 'POST':
        first_name = request.json.get('first_name', '').strip().lower()
        last_name = request.json.get('last_name', '').strip().lower()
        age = request.json.get('age', 0)

        if not isinstance(age, int) or not (0 <= age < 120):
            return json(Results.AGE_NOT_VALID)
        if first_name and last_name:
            user = await User.find_one(dict(first_name=first_name, last_name=last_name))
            if not user:
                await User.insert_one(dict(first_name=first_name, last_name=last_name, age=int(age)))
                return json(Results.USER_ADDED_SUCCESSFULLY)
            else:
                return json(Results.USER_ALREADY_EXISTS)
        else:
            return json(Results.NAME_EMPTY)
    else:
        first_name = request.args.get('first_name', '').strip().lower()
        last_name = request.args.get('last_name', '').strip().lower()
        age = request.args.get('age', None)
        search = {
            "first_name": {'$regex': ".*%s.*" % first_name},
            "last_name": {'$regex': ".*%s.*" % last_name},
        }
        if age:
            search["age"] = int(age)
        cur = await User.find(request, search)  # due to a bug, sending request as well
        return json({"users": str(cur.objects)})
