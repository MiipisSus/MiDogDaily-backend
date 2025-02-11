from sqlmodel import SQLModel


class AuthLogin(SQLModel):
    username: str
    password: str
    
class AuthLoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: 'AuthLoginUser'
    
class AuthLoginUser(SQLModel):
    id: int
