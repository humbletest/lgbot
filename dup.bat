cd ..
md %1
md %1\.vscode
xcopy lgbot\.vscode %1\.vscode /E /Y
md %1\book
xcopy lgbot\book %1\book /E /Y
md %1\chess
xcopy lgbot\chess %1\chess /E /Y
md %1\driver
xcopy lgbot\driver %1\driver /E /Y
md %1\engines
xcopy lgbot\engines %1\engines /E /Y
md %1\firebase
xcopy lgbot\firebase %1\firebase /E /Y
md %1\lbot
xcopy lgbot\lbot %1\lbot /E /Y
md %1\serverutils
xcopy lgbot\serverutils %1\serverutils /E /Y
md %1\static
xcopy lgbot\static %1\static /E /Y
md %1\templates
xcopy lgbot\templates %1\templates /E /Y
md %1\test
xcopy lgbot\test %1\test /E /Y
md %1\transcrypt
xcopy lgbot\transcrypt %1\transcrypt /E /Y
xcopy lgbot\*.* %1\ /E /Y
cd %1
echo doctor
pause
python doctor.py %1
echo create app
pause
rd .git /S /Q
git init
heroku destroy %1
heroku create %1
heroku stack:set heroku-18 -a %1
echo create virtual env
pause
pipenv --python C:\Unzip\Tools\Miniconda\python.exe
pipenv install
