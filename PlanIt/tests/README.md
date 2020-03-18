# Tests

Within this folder are test functions for the core calculations of PlanIt.

Before you begin, please make sure you write a configuration file as follows:
  ~/.hscfg
that contains:

```hs_endpoint = https://developer.nrel.gov/api/hsds
hs_username = None
hs_password = None
hs_api_key = 3K3JQbjZmWctY0xmIfSYvYgtIcM3CN0cb1Y2w9bf```


Please [follow this link](https://developer.nrel.gov/signup/) to get your own API key.

Clone the repository to your machine.

Then, in order to run tests using `nosetests`, in your terminal, navigate to the repository and then to the PlanIt folder.

Use the command `nosetests tests/test_example.py`.
