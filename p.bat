git add .
git reset -- transcrypt/app.py
git reset -- static/js/app.js
git reset -- bdef.yml.cache

git commit -m "%*"

git add transcrypt/app.py
git add static/js/app.js
git add bdef.yml.cache

git commit -m "%* bin"

git push heroku master

pause

git push origin master

