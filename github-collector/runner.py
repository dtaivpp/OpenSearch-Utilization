"""
Module used to run the collector and indexers
"""
import asyncio
from indexer import index_batch, create_index, create_client
from collector import repo_collector

def main():
  """Main method for github-collector"""
  opensearch = create_client()
  create_index(opensearch)

  loop = asyncio.get_event_loop()
  loop.run_until_complete(index_batch(opensearch, repo_collector))

if __name__=="__main__":
  main()
