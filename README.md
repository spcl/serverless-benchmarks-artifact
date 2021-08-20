
SeBS is a serverles benchmark suite designed to evaluate and model the performance and cost of FaaS platforms. The artifact has four main components:

* our tool with benchmarks and dependencies

* results obtained by us for the paper

* analysis of results

* scripts helping to reproduce most of the results in the paper.

First, we describe the source code, data and tooling provided with the [artifact](#artifact). Then, we describe the [environment and software packages necessary](#environment) and how to install it automatically or use with Docker. Please read it and follow instructions to properly initialize the environment. Then, we describe [results](#results) obtained in the paper and present scripts use to [reproduce them](#reproduction).

# Artifact

The entire artifact has been made publicly available under the DOI: `10.5281/zenodo.5209001`

With our artifact we provide the following components:

* `serverless-benchmarks` - source code of the benchmark suite
* `data` - benchmarking results obtained for the paper
* `analysis` - Python plotting and analysis scripts used for data analysis
* `experiments` - scripts helping to reproduce the experiments
* `docker` - compressed Docker images which were used for these experiments.

Our data has been obtained in January 2020, July and August 2020, and November 2020.

# Environment

All experiments analyze the performance of three commercial serverless offerings: [AWS Lambda](https://aws.amazon.com/lambda/), [Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/), and [Google Cloud Functions](https://cloud.google.com/functions).

To conduct the experiments, it is necessary to have an account on the platform. Our documentation helps to create credentials needed to use tool (details in `serverless-benchmarks/docs/platforms.md`). 

## Requirements & Installation

* Python 3.7 to install and use the benchmarking suite.
* Docker 19+ to build and deploy functions
* `libcurl` and its headers must be available on your system to install `pycurl`
* Standard Linux tools

First, clone the repository with the SeBS submodule:

```
git clone --recursive https://github.com/spcl/serverless-benchmarks-artifact.git
```

To install the benchmarks with a support for all platforms, run in the `serverless-benchmarks` the following command:

```
./install.py --aws --azure --gcp --local
```

It will create a virtual environment in `python-virtualenv`, install necessary Python dependencies and third-party dependencies. Then activate the new Python virtual environment, e.g., with `source python-virtualenv/bin/activate`. The environment must be always active when working with SeBS.

The the Docker daemon must be running and the user needs to have sufficient permissions to use it. Otherwise you might experience many "Connection refused" and "Permission denied" errors when using SeBS.

The software has been tested and evaluated on Linux (Debian, Ubuntu). We cannot guarantee that it is going to to operate correctly on systems as WSL.

## Docker

We use Docker images to build the packages of serverless functions and manage the Azure CLI. The Docker images can be pulled from our Docker Hub repository `spcleth/serverless-benchmarks`, they can be rebuilt manually by running `tools/build_docker_images.py` in SeBS main directory, and the most important images are provided as compressed archives in the `docker` subdirectory. Use `docker/load.sh` to load them.

## Results

The provided data is processed with a set of Python scripts, Jupyter notebooks, and R scripts.

The processing scripts are seperated between sections and research questions. Each subdirectory contains a `README.md` file describing the generation process and used datasets from the main `data` directory.

### Performance Analysis (Section 6.2)

* **Q1** - `performance/q1_perf/plot_time.py` generates Figure 3 in the paper.

* **Q2** - `performance/q2_cold/plot_cold_startups.py` generates Figure 4 in the paper.

* **Q3** - `performance/q3_portability/run.sh` generates the memory data cited in the section.

* **Q4** - `performance/q4_iaas/` contains the scripts to regenerate contents of Table 5.
Please follow the include `README.md` for details.

### Cost Analysis (Section 6.3)

* **Q1, Q2** - the notebook `cost/q1_cost/plots.ipynb` generates Figures 5a and 5b in the paper.

* **Q4** - `cost/q3_iaas_breakpoint/` contains the scripts to regenerate contents of Table 6.
Please follow the include `README.md` for details.

### Invocation Overhead (Section 6.4)

* **Q1** - the R script `invoc_overhead/parse_inv_overhead.R` generates Figure 6 in the paper.

### Container Eviction Modeling (Section 6.5)

* **Q1** - Python and R scripts wrapped under `container_eviction/run.sh` generate Figure 7 in the paper.

## Reproduction

1. After installing the benchmark suite and activating the virtual environment, create and configure cloud accounts according to the provided instructions in `serverless-benchmarks/docs/platforms.md`.

2. For all platforms, define the environmental variables storing cloud credentials.

3. Then, repeat the experiments according to the instructions provided for each benchmark.

### Perf-Cost

This experiment generates data for the main results from Sections 6.2 and 6.3. There are three directories `experiments/perf_cost/{provider}` with provider being `aws`, `azure` and `gcp`.

* For each platform, we repeat the generation of results for each benchmark used in the paper and with multiple memory sizes except for Azure.
* For each benchmark, we measure warm and cold invocations on AWS and GCP, and warm and burst invocations on Azure.
* For each execution we need 200 datapoints, and we perform 250 repetitions as the cloud billing system is not always reliable and it is not guaranteed that we will obtain exact billing data for each invocation.
* For cold experiments we need to enforce container eviction between each batch of invocations. Thus, the process can take several minutes.
* On Azure we no longer use the `thumbnailer` Node.js benchmark, as it is no longer possible
to create Linux function app with Functions runtime 2.0 and Node.js.

Steps needed to reproduce the results.

1. Make sure that credentials are configured and the `python-virtualenv` from SeBS installation is activated.

2. Execute the `run.sh` script which will run the SeBS experiment for each benchmark.

3. In each subdirectory, the out.log file will contain multiple invocation results such as this - one entry for each memory configuration.

   ```json
   12:40:05,907 INFO AWS-8915: Published new function code
   12:40:05,907 INFO Experiment.PerfCost-2b82: Begin cold experiments
   12:40:17,684 INFO Experiment.PerfCost-2b82: Processed 0 samples out of 50,0 errors
   12:40:17,684 INFO Experiment.PerfCost-2b82: Processed 0 warm-up samples, ignore results.
   12:40:34,509 INFO Experiment.PerfCost-2b82: Processed 10 samples out of 50,0 errors
   12:40:51,782 INFO Experiment.PerfCost-2b82: Processed 20 samples out of 50,0 errors
   12:41:08,634 INFO Experiment.PerfCost-2b82: Processed 30 samples out of 50,0 errors
   12:41:25,366 INFO Experiment.PerfCost-2b82: Processed 40 samples out of 50,0 errors
   12:41:42,509 INFO Experiment.PerfCost-2b82: Processed 50 samples out of 50,0 errors
   12:41:47,515 INFO Experiment.PerfCost-2b82: Mean 1538.35586, median 1475.9135, std 130.46677776369125, CV 8.480923117729812
   12:41:47,517 INFO Experiment.PerfCost-2b82: Parametric CI (Student's t-distribution) 0.95 from 1500.9011734974968 to 1575.810546502503, within 2.4347218661424113% of mean
   12:41:47,517 INFO Experiment.PerfCost-2b82: Non-parametric CI 0.95 from 1464.246 to 1511.239, within 1.591997091970496% of median
   12:41:47,519 INFO Experiment.PerfCost-2b82: Parametric CI (Student's t-distribution) 0.99 from 1488.4066173484066 to 1588.3051026515932, within 3.246923806796777% of mean
   12:41:47,519 INFO Experiment.PerfCost-2b82: Non-parametric CI 0.99 from 1459.516 to 1578.257, within 4.0226273423205345% of median
   12:41:47,532 INFO Experiment.PerfCost-2b82: Begin warm experiments
   12:41:53,636 INFO Experiment.PerfCost-2b82: Processed 0 samples out of 50,0 errors
   12:41:53,636 INFO Experiment.PerfCost-2b82: Processed 0 warm-up samples, ignore results.
   12:42:04,584 INFO Experiment.PerfCost-2b82: Processed 10 samples out of 50,0 errors
   12:42:15,446 INFO Experiment.PerfCost-2b82: Processed 20 samples out of 50,0 errors
   12:42:26,351 INFO Experiment.PerfCost-2b82: Processed 30 samples out of 50,0 errors
   12:42:37,383 INFO Experiment.PerfCost-2b82: Processed 40 samples out of 50,0 errors
   12:42:48,319 INFO Experiment.PerfCost-2b82: Processed 50 samples out of 50,0 errors
   12:42:53,322 INFO Experiment.PerfCost-2b82: Mean 874.2798799999999, median 893.336, std 58.710030168835715, CV 6.7152443413012906
   12:42:53,324 INFO Experiment.PerfCost-2b82: Parametric CI (Student's t-distribution) 0.95 from 857.4252767652275 to 891.1344832347723, within 1.9278269602604161% of mean
   12:42:53,324 INFO Experiment.PerfCost-2b82: Non-parametric CI 0.95 from 885.337 to 918.449, within 1.853278049916267% of median
   12:42:53,325 INFO Experiment.PerfCost-2b82: Parametric CI (Student's t-distribution) 0.99 from 851.802728396723 to 896.7570316032769, within 2.5709331894126377% of mean
   12:42:53,325 INFO Experiment.PerfCost-2b82: Non-parametric CI 0.99 from 821.185 to 920.821, within 5.576625144402558% of median
   ```

4. Inside each benchmark subdirectory, there will be a `perf-cost` subdirectory with JSON results for each

5. After few minutes, run `process.sh` to download cloud billing results and generate the output. **The waiting period is important, because not each cloud provider publishes billing logs immediately after the invocation**.

6. Inside each benchmark subdirectory, there will be a `perf-cost`  subdirectory with `result.csv` file. This file contains a summary of performance and cost data which we use for plotting and generation of tables.



