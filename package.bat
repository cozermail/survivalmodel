python manage.py collectstatic --noconfirm
pyinstaller .\manage.spec --noconfirm
md .\dist\manage\sklearn\.libs
copy .\dist\manage\lib\site-packages\sklearn\.libs\* .\dist\manage\sklearn\.libs