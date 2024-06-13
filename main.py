import uvicorn # type: ignore
from fastapi import FastAPI, Form, Request, Depends, HTTPException, status # type: ignore
from fastapi.responses import HTMLResponse, RedirectResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from sqlalchemy.orm import Session # type: ignore
from passlib.context import CryptContext # type: ignore
from models import User
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...),
    db: Session = Depends(get_db)
    ):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash the password
    hashed_password = get_password_hash(password)

    # Create a new User object
    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    # Add to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    # Redirect to the homepage or login page
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND) 

@app.get("/welcome")
async def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.post("/signin")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Authenticate the user
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
        )
        
    return RedirectResponse(url=f"/welcome?username={user.username}", status_code=status.HTTP_302_FOUND) 

if __name__ == "__main__":
    uvicorn.run( app, host="localhost", port=8000)