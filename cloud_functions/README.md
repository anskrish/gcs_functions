#GCP Cloud functions to Manage resources

##Below terraform will create cloud function and configure cloudscheduler to run at every day 9PM PST

##This script will store the resources statefile in GCS bucket and manage the statefile from GCS

#Execution steps

```
make set
make plan
make apply

```
