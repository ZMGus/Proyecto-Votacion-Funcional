from pydantic import BaseModel, EmailStr

class AdminAuth(BaseModel):
    email: str
    password: str
    
class AdminCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    password: str

class AdminResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str

    class Config:
        orm_mode = True