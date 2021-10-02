"""A collection of helper functions"""
from time import sleep
from opensearchpy import OpenSearch

def livelyness_poller(client: OpenSearch):
  """Checks to see if the cluster is alive"""
  status = None
  backoff = 1

  while status != "green" or status != "yellow":
    try:
      health = client.cluster.health()
      status = health['status']
    except:
      sleep(backoff)
      backoff = backoff + 2
