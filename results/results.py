class Results:
    RATE_LIMIT = {'result_code': "429", 'result_message': 'Too Many Requests', },
    USER_ADDED_SUCCESSFULLY = {"result_code": "0", "result_message": "User was added successfully."},
    USER_ALREADY_EXISTS = {"result_code": "-1", "result_message": "User already exists."},
    NAME_EMPTY = {"result_code": "-2", "result_message": "first_name and last_name cannot be empty"}
