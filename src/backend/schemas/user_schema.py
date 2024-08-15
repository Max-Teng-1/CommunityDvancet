from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: int
    avatar: str = None
    phone: str = None

class Login(BaseModel):
    email: str
    password: str


class PwdVerify(BaseModel):
    password: str

class Register(BaseModel):
    email: str
    password_1: str
    password_2: str
    username: str
    role: int

class PwdResetRequest(BaseModel):
    email: str

class PwdResetReset(BaseModel):
    reset_code_input: str
    reset_code_generate: str
    email: str
    password_1: str
    password_2: str

class PwdReset(BaseModel):
    password_old: str
    password_1: str
    password_2: str

class Id(BaseModel):
    id: int

class Update(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    email_notification: bool

class SecurityKey(BaseModel):
    security_key: str
    password: str
