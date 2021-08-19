multiprocessing.pool.RemoteTraceback: 
"""
Traceback (most recent call last):
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 110, in run
    final_results = [result.get() for result in results]
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 110, in <listcomp>
    final_results = [result.get() for result in results]
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 119, in worker
    result = (True, func(*args, **kwds))
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 73, in test
    raise RuntimeError('First invocation not cold on time {t} rep {rep} pid {pid} tid {tid}'.format(t=self._sleep_time,rep=repetition,pid=self._pid,tid=self._tid))
RuntimeError: First invocation not cold on time 15 rep 0 pid 0 tid 4
"""

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "scripts/cloud_experiments.py", line 182, in <module>
    cache_client=cache_client
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 243, in __init__
    ret = result.get()
  File "/usr/lib64/python3.6/multiprocessing/pool.py", line 644, in get
    raise self._value
RuntimeError: First invocation not cold on time 15 rep 0 pid 0 tid 4
