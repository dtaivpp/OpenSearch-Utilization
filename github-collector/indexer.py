"""
Module used for indexing repository data from GitHub
"""
import asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_streaming_bulk


def create_client():
  """Returns OpenSearch Client"""
  return AsyncElasticsearch(["https://opensearch-node1:9200","https://opensearch-node2:9200"])


def create_index(client):
  """Creates an index in OpenSearch"""
  client.indices.create(
    index="github",
    body={
      "settings": {"number_of_shards": 1}
    },
    ignore=400,
  )


async def index_batch(client: AsyncElasticsearch, data_generator):
  """Indexes a stream of documents"""
  async for ok, result in async_streaming_bulk(client, data_generator()): # pylint: disable=C0103
    action, result = result.popitem()
    if not ok:
      print("failed to %s document %s" % (action, result))


if __name__ == "__main__":
  _client = AsyncElasticsearch(["https://opensearch-node1:9200","https://opensearch-node2:9200"])
  create_index(_client)
