nohup python3 manage.py runserver --noreload 0.0.0.0:8001 >nohup.out 2>&1 &
tail -f nohup.out