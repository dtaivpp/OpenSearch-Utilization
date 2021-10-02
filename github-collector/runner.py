"""
Module used to run the collector and indexers
"""
import asyncio
from indexer import index_batch, create_index, create_client
from collector import repo_collector
from helpers import livelyness_poller

def main():
  """Main method for github-collector"""
  opensearch = create_client()

  livelyness_poller(opensearch)

  create_index(opensearch)
  opensearch_as = create_client(isasync=True)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(index_batch(opensearch_as, repo_collector))

if __name__=="__main__":
  main()
