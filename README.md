# fastapi-async-perf

```
fastapi run --workers 2 app.py
locust --headless -u 500 -r 50 -t 5m -f locustfile.py -H http://0.0.0.0:8000 AsyncConcurrentUser # change to user class: AsyncIndependentUser, AsyncDependentUser, AsyncConcurrentUser
```
