"""
Module used for indexing repository data from GitHub
"""
from opensearchpy import AsyncOpenSearch
from opensearchpy.helpers import async_streaming_bulk


def create_client():
  """Returns OpenSearch Client"""
  return AsyncOpenSearch(["https://opensearch-node1:9200","https://opensearch-node2:9200"])


async def create_index(client):
  """Creates an index in OpenSearch"""
  client.indices.create(
    index="github",
    body={
      "settings": {"number_of_shards": 1}
    },
    ignore=400,
  )


async def index_batch(client: AsyncOpenSearch, data_generator):
  """Indexes a stream of documents"""
  async for ok, result in async_streaming_bulk(client, data_generator()): # pylint: disable=C0103
    action, result = result.popitem()
    if not ok:
      print("failed to %s document %s" % (action, result))


if __name__ == "__main__":
  _client = AsyncOpenSearch(["https://opensearch-node1:9200","https://opensearch-node2:9200"])
  create_index(_client)
