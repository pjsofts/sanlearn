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
        age = request.json.get('age', '')
        if first_name and last_name:
            is_uniq = await User.is_unique(doc=dict(first_name=first_name, last_name=last_name))
            if is_uniq in (True, None):
                await User.insert_one(dict(first_name=first_name, last_name=last_name, age=int(age)))
                return json(Results.USER_ADDED_SUCCESSFULLY)
            else:
                return json(Results.USER_ALREADY_EXISTS)
        else:
            return json(Results.NAME_EMPTY)
    else:
        cur = await User.find()
        return json({"users": str(cur.objects)})
