# Users API
___
## API Calls
___
### Session
`session.py` holds the `/api/user/session` route, which handles all the needed CRUD database operations for sessions as well
as verifying valid sessions:
- **[POST]** `/api/user/session/create`:  Authenticates a user's credentials and assigns them a session id that is stored in the
    browser as a cookie. This session is valid for 3 hours or until the user logs out.
- **[GET]**  `/api/user/session/validate`: Verifies session for the user based on value of the session id. If session id has
    expired or is invalid, it will be revoked and return an Error status. If session id is valid it will return a
    Success status.
- **[DELETE]**  `/api/user/session/delete`: revokes session for the user based on value of session id. If session is invalid or does
    not exist, it will return an Error status. If session exists (valid or not) it will be revoked and it will return a
    Success status.
### User
`user.py` holds the `/api/user` route, which handles all the needed CRUD database operations for users as well as
getting the permission level for a user:
- **[POST]** `/api/user/register`: Creates a new user with the provided information. Adds an entry for both the users
    and logins tables. If unable to create new user, an Error status will be returned. If creation is successful, a 
    Success status is returned.
- **[GET]** `/api/user`: Fetches user data, formats it as a JSON object and returns it to the front end. If it is
    unable to find user data, it will return an Error status. If the fetch was successful, it will return a Success status
- **[PATCH]** `/api/user/update`: Updates users data with the provided information. Searches request body for valid
    update fields, then generates queries to update the user's data. If it is unable to update one of the fields, it will
    return an Error status. If it is able to update all fields successfully, it will return a Success status. It will
    ignore any invalid fields in the body, but it will not write the updates unless all updates are successful.
- **[DELETE]** `/api/user/delete`: Removes user based on session id. If unable to delete user, an Error status will be 
    returned. If deletion is successful, a Success status is returned. **In future updates to the users api, a user will
    be able to be removed based on a specified account id.**
- **[GET]** `/api/user/permissions`: Fetches permissions for user based on session id, formats it as a JSON object and
    returns it to the front end. If it is unable to find user data, it will return an Error status. If the fetch was
    successful, it will return a Success status