multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 125, in run
    final_results = [result.get() for result in results]
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 125, in <listcomp>
    final_results = [result.get() for result in results]
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 75, in test
    first_data = invoke(tid, repetition, url, json_data)
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 34, in invoke
    'code {code}! Reason: {reason}').format(**data)
RuntimeError: Request 0 at 2020-02-01 20:33:39.545371 for https://010-sleep-python-50d9a9d6-128-1-17-2.azurewebsites.net/api/handler?code=O7lPfeaU3q42m2RlfvdpVkYBOCkQ0pojbkHlkRa4NOArj26l7tL3uw== finished with statuscode 503! Reason: Site Unavailable
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "scripts/cloud_experiments.py", line 191, in <module>
    cache_client=cache_client
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 267, in __init__
    ret = result.get()
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
RuntimeError: Request 0 at 2020-02-01 20:33:39.545371 for https://010-sleep-python-50d9a9d6-128-1-17-2.azurewebsites.net/api/handler?code=O7lPfeaU3q42m2RlfvdpVkYBOCkQ0pojbkHlkRa4NOArj26l7tL3uw== finished with statuscode 503! Reason: Site Unavailable
