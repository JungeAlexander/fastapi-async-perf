# fastapi-async-perf

```
fastapi run --workers 2 app.py
locust --headless -u 500 -r 50 -t 5m -f locustfile.py -H http://0.0.0.0:8000 AsyncConcurrentUser # change to user class: AsyncIndependentUser, AsyncDependentUser, AsyncConcurrentUser
```

# Blog post - Basic async performance testing with FastAPI and Locust

[FastAPI](https://fastapi.tiangolo.com/) sync vs async performance testing

[Locust](https://locust.io/) for load testing

Springle in a bunch of `async` and `await` to hope for the best.

Besides useful but basic concurrency [explanations](https://fastapi.tiangolo.com/async/#asynchronous-code), little guidance on how to actually improve async performance in a real application.

use `asyncio.sleep()` to simulate a slow task, e.g. database lookup, external API call (including to a language model or other AI service)

## Takeaways

### High throughput

- async/await enough

### Low latency

- gather needed

Lots of factors - how served, workers, etc. (running this locally on my laptop)

- Baseline: 3 sync tasks
- Async: 3 async tasks in order (indepedent)
- Async: 3 async tasks in order (dependent)
- Async: 3 async tasks in parallel

## Drawing

dependent and independent: runtime figure out dependency between functions, does not seem to be the case.


Side note: I tried to work out the math behind this but cannot make it work. I guess there is just too much complexity even in this simple setup for a back of the envelope calculation to make sense.
Of course, these practical results are what matter.

Code is available here: https://github.com/JungeAlexander/fastapi-async-perf 


```
Type     Name                                                       # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /sync_baseline                                               1520     0(0.00%) |  79082   15026  119366  76000 |    5.29        0.00
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                   1520     0(0.00%) |  79082   15026  119366  76000 |    5.29        0.00

Response time percentiles (approximated)
Type     Name                                                               50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /sync_baseline                                                   76000  96000 105000 105000 106000 119000 119000 119000 119000 119000 119000   1520
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                       76000  96000 105000 105000 106000 119000 119000 119000 119000 119000 119000   1520


+++++++++++++++++

Type     Name                                                       # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /async_independent                                           9500     0(0.00%) |  15021   15002   15140  15002 |   32.24        0.00
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                   9500     0(0.00%) |  15021   15002   15140  15002 |   32.24        0.00

Response time percentiles (approximated)
Type     Name                                                               50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /async_independent                                               15000  15000  15000  15000  15000  15000  15000  15000  15000  15000  15000   9500
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                       15000  15000  15000  15000  15000  15000  15000  15000  15000  15000  15000   9500


+++++++++++++++++

Type     Name                                                       # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /async_dependent                                             9500     0(0.00%) |  15020   15003   15093  15003 |   32.25        0.00
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                   9500     0(0.00%) |  15020   15003   15093  15003 |   32.25        0.00

Response time percentiles (approximated)
Type     Name                                                               50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /async_dependent                                                 15000  15000  15000  15000  15000  15000  15000  15000  15000  15000  15000   9500
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                       15000  15000  15000  15000  15000  15000  15000  15000  15000  15000  15000   9500

+++++++++++++++++

Type     Name                                                       # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /async_concurrent                                           29157     0(0.00%) |   5018    5001    5477   5001 |   97.33        0.00
--------|---------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                  29157     0(0.00%) |   5018    5001    5477   5001 |   97.33        0.00

Response time percentiles (approximated)
Type     Name                                                               50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /async_concurrent                                                 5000   5000   5000   5000   5000   5100   5100   5100   5300   5500   5500  29157
--------|-------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                        5000   5000   5000   5000   5000   5100   5100   5100   5300   5500   5500  29157
```