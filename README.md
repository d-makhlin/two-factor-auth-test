# two-factor-auth-test

test problem with a 2fa service

## How to run this project

1. Clone this repository and

   $ git clone https://github.com/d-makhlin/two-factor-auth-test.git

   $ cd two-factor-auth-test

2. Start the project via docker

   $ docker-compose build

   $ docker-compose up -d

3. Take a look at API contracts at 'localhost:8000/docs/'

4. Send POST 'localhost:8000/api/users/auth/register/' request according to the swagger docs

   with a header 'Content-type: application/json'

5. If you've set 'use_two_step_auth' as False, you may use /login request to log in

6. If not, you should follow the link you receive with /register response. Afterwards you may login.
