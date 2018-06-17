git checkout public

git merge --squash master

pause

del firebase\*.json

git add .
git reset -- transcrypt/app.py
git reset -- static/js/app.js
git reset -- bdef.yml.cache
git reset -- binid.txt
git reset -- localconfig.json

git commit -m "%*"

git add transcrypt/app.py
git add static/js/app.js
git add bdef.yml.cache
git add -- binid.txt
git add -- localconfig.json

git commit -m "%* bin"

pause

git push lgbot public
