
The results represent the Table 5 in the paper.

### IaaS data

First two rows are represented in `aws_minio_results.txt` and `aws_s3_results.txt`.

Run `run.sh` to recompute them - it runs `statistics.py` to compute the statistics.

Then, we select the warm values for each benchmark, and write the data into the file `faas_statistics.py`.
The data is divided by 1000 to convert from milliseconds to seconds.
**This step is manual**.

Source of data: `data/performance/iaas_results`.

### FaaS data

The script `faas_statistics.py` computes the FaaS statistics and generates table data, using
the data provided in previous step as well.

The results, including table data, are in the `final_table.txt` file.

Source of data: `data/performance/{provider}_perf_cost`, where `provider` is `aws`, `azure`, or `gcp.
