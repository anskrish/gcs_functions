import functions_framework
import time
import json
import os
import requests
import re
from datetime import datetime
from datetime import date 
from google.cloud import compute_v1
from google.cloud import container_v1beta1
from prettytable import PrettyTable

@functions_framework.http
def delete_resources(request):
    try:
        project_id = os.environ.get("PROJECTID")
        table = PrettyTable()
        today = date.today()
        table.field_names = ["Resource Name", "Resource Type"]
        client = container_v1beta1.ClusterManagerClient()
        request = container_v1beta1.ListClustersRequest(
            project_id= project_id,
            zone="-"
        )
        response = client.list_clusters(request=request)
        clusters = response.clusters
        for cluster in clusters:
          cluster_name = cluster.name
          # add delete logic based on labels
          print(f"cluster name: {cluster_name} -- {cluster.current_node_count} -- labels: {cluster.resource_labels}")
          if 'delete_after' in cluster.resource_labels:
            match = re.search(r'\d{2}-\d{2}-\d{4}', cluster.resource_labels['delete_after'])
            delete_date = datetime.strptime(match.group(), '%m-%d-%Y').date()
            difference = delete_date - today
            if difference.days < 0:
              print(f"{cluster_name} is for delete")
              delete_gke_request = container_v1beta1.DeleteClusterRequest(project_id=project_id,zone=location,cluster_id=cluster_name,)
              # delete_response = client.delete_cluster(request=request)
              # print(f"{cluster_name} delete response {delete_response}")
          else:
            table.add_row([cluster_name, "GKE Cluster"])

        
        # compute Clients
        compute_client = compute_v1.InstancesClient()
        zones_request = compute_v1.ZonesClient().list(project=project_id)
        all_zones = [zone.name for zone in zones_request.items]
        print(all_zones)
        for zone in all_zones:
          req = compute_v1.ListInstancesRequest(project=project_id, zone=zone)
          response = compute_client.list(request=req)
          for inst in response.items:
            print(f"{inst.name}'s labels {inst.labels} and {inst.name.find('nodepool')}")
            # add logic to delete the cluster based on labels
            if 'goog-k8s-cluster-name' not in inst.labels:
              if 'delete_after' in inst.labels:
                match = re.search(r'\d{2}-\d{2}-\d{4}', inst.labels['delete_after'])
                delete_date = datetime.strptime(match.group(), '%m-%d-%Y').date()
                difference = delete_date - today
                if difference.days < 0:
                  #Need to delete the resource as per the date label
                  print(f"{inst.name} is for delete")
                  delete_inst_request = compute_v1.DeleteInstanceRequest(instance=inst.name, project=project_id, zone=zone)
                  # delete_response = client.delete(request=request)
                  # print(f"{inst.name} delete response {delete_response}")
              else:
                table.add_row([inst.name, "VM Instance"])
          
    except Exception as e:
        print(f"an error occured {e}")

    print(f"Numbe of GKE clusters to delete {len(table.rows)}\n")
    print(table.get_string())
    send_slack_notification(table)
    return 'completed'
  
def send_slack_notification(table):
    URL = os.environ.get("SLACK_URL")
    HEADERS = {"content-type":"application/json"}
    message = ""
    if len(table.rows) > 0:
      message = "The following resources are not labeld with `delete_after` \n\n" + table.get_string()
    else:
      message = "All the resources are  labeld with `delete_after`"  
       
    
    salck_payload = json.dumps({"text" : message + '\n\n Please add `delete_after` label to your resources'})
    print(salck_payload)
    r = requests.post(URL, data=salck_payload, headers=HEADERS)
    print(r.status_code, r.reason)
