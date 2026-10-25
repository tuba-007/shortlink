*24 Oct 2026*
Git  : Refreshed my basics about git : 
- main / master : the local repository/folder we have on  our disk
- origin : the remote server/location where we are goingt to push or store our main/master
- git init  : creates a hidden .git folder in our directory, to initialise a repo , basically asking git to track it (we still need to ass git add and commit to track)
- git push -u origin master :  "push my local master/main(if we renamed it to main) branch to origin, and -u remembers the link so next time git push is enough."
- git branching : git checkout -b <branchname> to create a branch
- full cycle done :  created a branch , raised pr , merged it and deleted it. 

*25 Oct 2026*
Python: FastAPI implementation:
- I used a virtual environment (venv) to keep packages separate, so they are limited to the ShortLink project.
- The command `python -m venv .venv` creates a `.venv` folder where all the project's packages are installed.
- Activate it in PowerShell with `.venv\Scripts\Activate.ps1`. The prompt then shows `(.venv)`.
- `.venv/` is listed in `.gitignore` so the folder is not committed to Git.

PIP - The python package Installer 
- pip install something downloads that package from PyPI (the Python Package Index, a public online store of packages) and puts it in your environment. It comes bundled with Python, so you probably didn't need to install it separately
- You can check what's installed : pip list
