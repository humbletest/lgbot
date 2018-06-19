git checkout master

echo off
git add .
git reset -- transcrypt/app.py
git reset -- static/js/app.js
git reset -- bdef.yml.cache
git reset -- binid.txt
git reset -- localconfig.json
echo on

git commit -m "%*"

echo off
git add transcrypt/app.py
git add static/js/app.js
git add bdef.yml.cache
git add -- binid.txt
git add -- localconfig.json
echo on

git commit -m "%* bin"

git push heroku master
