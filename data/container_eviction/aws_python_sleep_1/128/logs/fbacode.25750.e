18:43:31,163 INFO Created experiment output at /users/mcopik/projects/serverless-benchmarks/experiments/prob_first_attempt/20
18:43:31,273 INFO Using cached storage input buckets []
18:43:31,273 INFO Using cached storage output buckets []
18:43:31,277 INFO Work on times [360, 480, 600, 720, 900, 1080, 1200]
18:43:31,277 INFO Work on urls []
18:43:31,277 INFO Using urls []
18:43:44,441 INFO Repeat update...
18:43:44,441 INFO An error occurred (TooManyRequestsException) when calling the UpdateFunctionConfiguration operation (reached max retries: 4): Rate exceeded
18:43:45,241 INFO Updated 010_sleep_python_128_128_1_20_360 to timeout 860
18:43:45,955 INFO Updated 010_sleep_python_128_128_1_20_360 to timeout 860
18:43:47,987 INFO Updated 010_sleep_python_128_128_1_20_480 to timeout 860
18:43:48,132 INFO Updated 010_sleep_python_128_128_1_20_480 to timeout 860
18:43:57,409 INFO Repeat update...
18:43:57,409 INFO An error occurred (TooManyRequestsException) when calling the UpdateFunctionConfiguration operation (reached max retries: 4): Rate exceeded
18:44:02,279 INFO Updated 010_sleep_python_128_128_1_20_600 to timeout 860
18:44:02,434 INFO Updated 010_sleep_python_128_128_1_20_600 to timeout 860
18:44:02,574 INFO Updated 010_sleep_python_128_128_1_20_720 to timeout 860
18:44:02,712 INFO Updated 010_sleep_python_128_128_1_20_720 to timeout 860
18:44:02,852 INFO Updated 010_sleep_python_128_128_1_20_900 to timeout 860
18:44:02,993 INFO Updated 010_sleep_python_128_128_1_20_900 to timeout 860
18:44:03,132 INFO Updated 010_sleep_python_128_128_1_20_1080 to timeout 860
18:44:03,278 INFO Updated 010_sleep_python_128_128_1_20_1080 to timeout 860
18:44:05,666 INFO Updated 010_sleep_python_128_128_1_20_1200 to timeout 860
18:44:05,807 INFO Updated 010_sleep_python_128_128_1_20_1200 to timeout 860
18:44:05,807 INFO Start 20 invocations with 7 times
multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 101, in run
    with ThreadPool(threads) as pool:
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 789, in __init__
    Pool.__init__(self, processes, initializer, initargs)
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 167, in __init__
    raise ValueError("Number of processes must be at least 1")
ValueError: Number of processes must be at least 1
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "scripts/cloud_experiments.py", line 182, in <module>
    cache_client=cache_client
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 242, in __init__
    ret = result.get()
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
ValueError: Number of processes must be at least 1
