
The results reproduces the Table 6 in the paper.
The results are obtained in three steps.

1. We use the `cost_analysis.py` script to generate the data in `faas_cost.txt` file.
The data presents the cost for 1M executions for each memory configuration.

2. The script `table_generator.py` requires manual input of three datasets:
- the warm IaaS performance for Minio and S3 that has been obtained in `performance/q4_iaas/`
and used there in the script `faas_statistics.py
- the 'performance' result of FaaS, taken from the result of previous step - we select the 
`true_gbs` cost for a memory configuration where we have the highest performance and further
memory increases don't bring major improvements (see Sec.6.3.Q3 for details)
- the 'eco' result of FaaS, taken from the result of previous step - similar to the previous
step, but we select the configuration with the lowest cost.

3. We run the `table_generator.py` script to generate the data for the table.
The result is stored in `final_table.txt`.

Source of data: `data/performance/iaas_invocations` and `data/performance/perf_cost`.

