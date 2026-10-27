# FastAPI builds the app; BaseModel describes the shape of data the client sends
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

# secrets picks random characters; string gives us ready-made letters and digits
import secrets
import string

# The app itself. Every door (endpoint) below is attached to it.
app = FastAPI()

# Door 1: GET /health. Answers "is the app alive?"
@app.get("/health")
def  health():
    return {"status": "ok"}

# Describes what the client must send to /shorten: JSON with a text field "url".
# If "url" is missing or not text, FastAPI replies with a 422 error by itself.
class ShortenRequest(BaseModel):
    url: str

# Temporary storage: {short code: long url}.
# It lives in memory, so it is emptied every time the server restarts.
# Postgres will replace this later.
link = {}
clicks = {}

# Makes a random short code, 6 characters long unless told otherwise, e.g. "aZ3kQ9"
def make_code(length=6):
    # the pool to pick from: a-z, A-Z and 0-9 (62 characters)
    chars=string.ascii_letters+string.digits
    # start with an empty code and add one character at a time
    code=""
    for i in range(length):
        # pick one random character from the pool
        random_char = secrets.choice(chars)
        # add it to the end of the code
        code = code+random_char
    # give the finished code back to whoever called the function
    return code

# Door 2: POST /shorten. Takes a long URL and gives back a short code.
@app.post("/shorten")
def shorten(body: ShortenRequest):
    long_url=body.url
    if not long_url.startswith(("http://" , 'https://')):
        long_url = "https://" + long_url
    # make a new random code
    code = make_code()
    # save it: code -> long url the client sent
    link[code] = long_url
    clicks[code] = 0
    # reply with the code and the full short link to share
    return {"code" : code , "short_url" : f"http://localhost:8000/{code}"}


@app.get("/{code}")
def redirect (code: str):
    long_url = link.get(code)
    if long_url is None:
        raise HTTPException(status_code=404,detail="Shorturl not found")
    clicks[code] = clicks[code]+1
    return  RedirectResponse(long_url)

@app.get("/status/{code}")
def getstatus (code : str):
    count = clicks.get(code)
    if count is None:
        raise HTTPException (status_code=404 , detail="Shorturl not found")
    return (f"This Url is visited {count} times")