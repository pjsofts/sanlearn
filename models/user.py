from sanic_motor import BaseModel


class User(BaseModel):
    __coll__ = 'users'
    __unique_fields__ = ['first_name', 'last_name']

    def __repr__(self):
        return str({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age
        })
