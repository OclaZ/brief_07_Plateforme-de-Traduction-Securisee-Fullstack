from pydantic import BaseModel, Field

class UserBase(BaseModel):
    id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True
class UserCreate(BaseModel):
    username: str
    password: str
class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str = Field(..., description="Nom d'utilisateur")
    password: str = Field(..., description="Mot de passe")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "admin  "
            }
        }


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT d'accès")
    token_type: str = Field(default="bearer", description="Type de token")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Message d'erreur")

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Nom d'utilisateur ou mot de passe incorrect"
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Texte à traduire")
    direction: str = Field(..., description="Direction de traduction ('en-fr' ou 'fr-en')")

    class Config:
        json_schema_extra = {
            "example": {
                     "text": "Hello, how are you?",
                     "direction": "en_fr"
}
        }

class TranslateResponse(BaseModel):
    text: str = Field(..., description="Texte en entrée")
    traduction: list = Field(..., description="Résultat de la traduction")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Très bon film, je le recommande vivement!",
                "traduction": [
                    {
                        "translation_text": "Very good movie, I highly recommend it!"
                    }
                ]
            }
        }
