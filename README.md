# BACKEND

## PROJECT DETAILS

There have 2 role here:
- User
- Admin

Routes of this project:
- Auth route `/auth` :
  - POST `/registration` : for register a user
  - POST `/login` : for login

- User route `/user` :
  - GET : for user to see their profile and all todo list

- Admin route `/admin` :
  - GET : to get all user profile
  - GET `/:user_id` : to get all todo list by user_id
  - GET `/todo` : to see all todo list
  - GET `/todo/:user_id` : to see all todo list by user_id
  - DELETE `/todo/:id` : to delete a todo list by todo id

- Todo route `/todo` :
  - POST : to make a new todo list
  - PUT `/:id` : to edit a todo list by todo id
  - PATCH `/:id` : to update status todo list by todo id
  - DELETE `/:id` : to delete a todo list by todo id

Here is the [link](https://serene-sierra-14359-bfd563eafed9.herokuapp.com/) of my backend.

Thankyou