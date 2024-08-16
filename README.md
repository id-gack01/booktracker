Hello, thanks for passing by. 

Here's my attempt at directing you guys on how to download and run the project. Make sure you have python installed please. 
First, try 
```
git clone https://github.com/id-gack01/booktracker.git
```
(I guess this implies that git is also installed, https://www.simplilearn.com/tutorials/git-tutorial/git-installation-on-windows, Linux has it installed iirc, 
and for Apple, https://git-scm.com/download/mac)

If that doesn't work...to make the directory
```
mkdir booktracker_app
cd booktracker_app
```

then (after git clone or directory made yourself)

```
python -m venv /path/to/new/virtual/environment
```
If unfamiliar with terminal/cmd prompt navigation, I would recommend doing copy as path and pasting that value into the /path/to thing you see. 
Left shift + right click on windows will allow the copy as path option to show up, works automatically in my manjaro linux, 
idk about apple, apple users can think different and look it up for themselves.

Below is what the docs say

###
On Windows, invoke the venv command as follows:
```
c:\>Python35\python -m venv c:\path\to\myenv
```
Alternatively, if you configured the PATH and PATHEXT variables for your Python installation:
```
c:\>python -m venv c:\path\to\myenv
```
###
(Below is if the booktracker directory doesn't make itself, I should add)
```
mkdir booktracker
cd booktracker
```
Make the booktracker directory now, this is where the work will get done.  Some future commands (init-db amongst them) require that they be fired in directories containing the whole project, so that's why the first directory was made.
Make sure you have pip installed. (https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)  (https://idroot.us/install-pip-manjaro/) (macOS Users can watch this - https://www.youtube.com/watch?v=5sMBhDv4sik).

```
pip install flask werkzeug
```


Next you gotta do...
```
cd ..
```
This takes you up into the booktracker_app directory you made. Do ls or dir to double check you're in the right place. Then run...
```
flask --app booktracker init-db
```
Allows you to interact with the sql lite3 database (sqlite3 is included in python, so no extra downloads)

then run...
```
cd booktracker
flask --app __init__.py run
```
The idea being you run the flask --app (filewheretheflaskappiscreated).py run command in that same directory so it can pick it up.
```app = Flask(__name__, instance_relative_config=True)```
is the creation of the app, and that's located in __init__.py.
to run the project in debug mode, adding --debug to the end will help. If you make changes, you'll immedaitely see them.

Typing  http://127.0.0.1:5000/testapp into the browser
should work at this point. If it doesn't, one of us messed up.

Can make a profile with the register link, that profile will hold your books. Don't forget the password because there's no recovery. 
I guess a PR would be to make it so no one but the logged in user can see only see *their* books in /authors or the comments and such of other profiles but for now, I'll just leave it.
I also need to look into how to host this project for free online somehow. 

Can check out the authors, can check out the completion status for each book, can see the number of pages and whatever comments got made. 

