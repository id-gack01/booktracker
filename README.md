Hello, thanks for passing by. 

Here's a my attempt at directing you guys on how to download and run the project. Make sure you have python installed please. 

try git clone https://github.com/id-gack01/booktracker.git

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
Left shit + right click on windows will allow the copy as path option to show up, works automatically in my manjaro linux, 
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
Make sure you have pip installed. (https://www.geeksforgeeks.org/how-to-install-pip-on-windows/)  (https://idroot.us/install-pip-manjaro/) (Apple Users can watch this - https://www.youtube.com/watch?v=5sMBhDv4sik).

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
flask --app __init__.py run
```
to run the project adding  to the end  --debug will help
Typing  http://127.0.0.1:5000/testapp into the browser
should work at this point.

Can make a profile with the register link, that profile will hold your books. Don't forget the password because there's no recovery. 
I guess a PR would be to make it so no one but the logged in user can see the books in /authors or the comments and such of other profiles but for now, I'll just leave it.
I also need to look into how to host this project for free online somehow. 

Can check out the authors, can check out the completion status for each book, can see the number of pages and whatever comments got made. 

