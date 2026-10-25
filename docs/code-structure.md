# ShortLink: Code Structure Cheat Sheet

Last updated: 2026-10-25

## Big picture

A request enters through uvicorn, FastAPI picks one function by method and path, and the answer travels back the same way.

```
request = method + path (+ JSON body)
Client ──▶ uvicorn ──▶ FastAPI app ──▶ Function ◀──▶ Storage
(browser,  (web server, (matches method (in main.py:   (link dict now,
 curl,      port 8000)   + path)         runs, returns)  Postgres later)
 or /docs)
   ▲                                        │
   └──── response = status code + JSON, or a redirect
```

The Function box is the only part I write: the functions in `main.py`. The rest is provided by the libraries.

## Project files

The whole app is one file, `main.py`; everything else supports it.

| File / folder | What it is | In Git? |
| --- | --- | --- |
| `main.py` | The app: model, storage, helper, doors | Yes |
| `.venv/` | Private toolbox of packages (FastAPI, uvicorn, pydantic) for this project only | No |
| `__pycache__/` | Python's auto-generated compiled cache; safe to delete | No |
| `.gitignore` | Tells Git what to skip: `.venv/`, `__pycache__/`, `*.pyc`, `.env` | Yes |
| `.env` (later) | Local secrets such as the database URL | No, never |
| `requirements.txt` (to add) | List of packages; made with `pip freeze > requirements.txt` | Yes |
| `ProjectPlan.md`, `docs.md`, `docs/` | Plan and my own notes | Yes |

## main.py, top to bottom

`main.py` has five parts, and the order matters: FastAPI matches doors in the order they are written.

1. **Imports**: `FastAPI` builds the app, `BaseModel` describes request bodies, `secrets` and `string` are standard library and build random codes.
2. **`app = FastAPI()`**: the building that holds every door.
3. **`class ShortenRequest(BaseModel)`**: the shape of the body for `POST /shorten`, one field `url: str`. FastAPI rejects anything else with a `422`.
4. **`link = {}`**: temporary storage, `{code: long_url}`, in memory. It is wiped on every server restart; Postgres replaces it.
5. **`make_code(length=6)`**: picks 6 random letters and digits with `secrets.choice` and joins them. About 56 billion combinations (62 to the power 6).

Then the doors:

```python
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/shorten")
def shorten(body: ShortenRequest):
    code = make_code()
    link[code] = body.url
    return {"code": code, "short_url": f"http://localhost:8000/{code}"}
```

How to read a door: the decorator `@app.<method>("<path>")` wires the function underneath to that method and path. Function parameters are how data arrives: `body: ShortenRequest` is the JSON body, and `code: str` (in `GET /{code}`) is the part of the path.

**Order rule:** `GET /{code}` matches any one-word path, so it must be written after `/health`, or it would swallow `/health` as a code.

## The four doors

Two are built; the redirect and stats doors are next.

| Door | What it does | Success | Errors | Status |
| --- | --- | --- | --- | --- |
| `GET /health` | Says the app is alive | `200` `{"status":"ok"}` | none | Built |
| `POST /shorten` | Takes `{"url": ...}`, makes a code, stores it, returns code and short URL | `200` code + short_url | `422` if `url` is missing | Built (dictionary storage) |
| `GET /{code}` | Looks up the code, adds 1 click, redirects to the long URL | `307` redirect | `404` unknown code | Next |
| `GET /stats/{code}` | Returns the click count | `200` code, long_url, clicks | `404` unknown code | After that |

To test: send the full URL with the scheme, `https://www.google.com`. Without `https://` the browser treats it as a path on your own server and will not leave it.

## Requests and status codes

A request has four parts: **method** (the verb), **path**, an optional **body**, and it gets back a **status code** plus a response body. A door is a method plus a path.

| Code | Meaning | When I see it |
| --- | --- | --- |
| `200` | OK | `/health`, `/shorten`, `/stats` worked |
| `307` | Temporary redirect | `GET /{code}` sends the browser to the long URL |
| `404` | No such door, or a code that is not stored | `/banana`, or an unknown short code |
| `405` | Door exists, wrong method | `POST /health` |
| `422` | Body failed validation | `POST /shorten` with `{}` |

`GET` reads, `POST` creates. That is why `/shorten` is a `POST` and `/{code}` is a `GET`.

Free docs: `http://localhost:8000/docs` is Swagger UI where every door can be tried; `/redoc` is the read-only version. FastAPI builds both from the code, so they update on every save.

## Commands

Environment and server (PowerShell, from the project folder):

```powershell
python -m venv .venv                 # create the venv (once)
.venv\Scripts\Activate.ps1           # switch it on (every new terminal); prompt shows (.venv)
pip install "fastapi[standard]"      # install packages into .venv
pip freeze > requirements.txt        # record the package list
fastapi dev main.py                  # run with auto-reload on http://localhost:8000
```

Stop the server with `Ctrl+C`. Leave the venv with `deactivate`.

Git flow for each change:

```bash
git status                           # look before adding
git checkout -b my-branch            # new branch
git add main.py                      # add files by name, not git add .
git commit -m "What changed"
git push -u origin my-branch         # then open a PR on GitHub and merge
git checkout master && git pull      # sync afterwards
```

When work seems lost: `git reflog` shows every commit `HEAD` has been on; `git branch rescue <hash>` saves one. `git rm -r --cached <path>` stops tracking a file without deleting it from disk.

## Gotchas so far

- **Server restart wipes the `link` dictionary.** Every save of `main.py` reloads the server, so a code made earlier returns `404`. Create the link again after the last save. Postgres fixes this.
- **Use the full URL when testing**, `https://www.google.com`, or the redirect has nowhere to go.
- **Port is `8000`**, not `8080`.
- **An empty `.gitignore` plus `git add .` stages the whole `.venv`** (3,230 files). Run `git status` first; fix with `git rm -r --cached .venv`.
- **A short link only works once the `GET /{code}` door exists**; until then it returns `404`.
- **A merged PR does not carry later commits.** Push to a branch after its PR is merged and you need a new PR.
- **`.venv` activation:** the prompt must show `(.venv)`, or `pip install` goes to the wrong place.

## Next in Phase 2

- [ ] `GET /{code}`: look up, redirect, `404` if unknown
- [ ] `GET /stats/{code}`: return the click count
- [ ] Postgres: create the table, replace the dictionary with SQL
- [ ] Click counter: add 1 on every redirect
- [ ] Config: database URL from an environment variable, not in code
- [ ] Notes: `docs/phase-2-app.md` and a log entry
