from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

app = FastAPI()

# Initialize password context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic model for signup request
class SignupRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# Dummy database simulation
fake_db = {}

# Function to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify email uniqueness
def is_email_unique(email: str) -> bool:
    return email not in fake_db

@app.post("/api/signup")
async def signup(request: SignupRequest):
    # Check if email is unique
    if not is_email_unique(request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the user's password
    hashed_password = get_password_hash(request.password)

    # Store user in the fake database
    fake_db[request.email] = {
        "username": request.username,
        "email": request.email,
        "password": hashed_password,
    }

    return {"message": f"User {request.username} signed up successfully."}
