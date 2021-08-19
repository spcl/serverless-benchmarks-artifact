Traceback (most recent call last):
  File "scripts/cloud_experiments.py", line 189, in <module>
    code_package=package,
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/scripts/CloudExperiments.py", line 284, in __init__
    MemorySize=memory
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/sebs-virtualenv/lib64/python3.6/site-packages/botocore/client.py", line 276, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/users2/mcopik/projects/serverless-benchmarks/serverless-benchmarks/sebs-virtualenv/lib64/python3.6/site-packages/botocore/client.py", line 586, in _make_api_call
    raise error_class(parsed_response, operation_name)
botocore.errorfactory.TooManyRequestsException: An error occurred (TooManyRequestsException) when calling the UpdateFunctionConfiguration operation (reached max retries: 4): Rate exceeded
