from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def create_index(client):
  """Creates an index in OpenSearch"""
  client.indices.create(
      index="github",
      body={
          "settings": {"number_of_shards": 1}
      },
      ignore=400,
  )


def index_batch(client: Elasticsearch, docs: list):
  """Indexes a list of documents"""
  bulk(index='github', doc_type='repository', body=docs)


if __name__ == "__main__":
    client = Elasticsearch()
    create_index(client)