##POSTMAN Collection Link
https://www.getpostman.com/collections/fca320416b70acd15c55

## List Users
list of users in Mongodb

GET http://localhost:8000/users

GET http://localhost:8000/users?first_name=pouria1&last_name=jahandideh2&age=20

## Add Users 
Add a new user with POST

POST http://localhost:8000/users


json data: {

	"first_name": "Pouria1112",
	
	"last_name": "Jahandideh13",
	
	"age": 540	
}

## Max 10
GET http://localhost:8000/max10?number=81

sample output
`{
    "max10": "[1, 2, 3, 4, 5]"
}`
    