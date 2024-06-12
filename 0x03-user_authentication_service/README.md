# User Authentication

User authentication is a vital point of an authentication-required application

Protecting an unauthorized user from accessing private resources

## Implementation Sample:

\_hash_password(password) -> bytes : Hash a user password and return the hashed password
AUTH = Auth()

AUTH.valid_login(email, password): Validates login credentials (Email and Password)
