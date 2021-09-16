from time import sleep
from ghapi.all import GhApi
from ghapi.page import paged
from pprint import pprint

api = GhApi()
rate_limits = {}

# Query to see current rate limits
def rate_limit():
  """Set the ratelimits context"""
  global rate_limit
  rate_limit = api.rate_limit()


def api_searcher(query: str) -> dict:
  """Searches for documents that match query string"""
  repos = paged(api.search.repos, per_page=100, q=query)

  for repo in repos:
    yield repo['items']


def repo_collector(query: str = "q=OpenSearch") -> dict:
  """Yeilds OpenSearch formatted documents that match the query"""
  searcher = api_searcher(query)

  for repo_list in searcher:
    for repo in repo_list:
      name, owner = repo['name'], repo['owner']['login']
      repo["tags"] = api.repos.list_tags(owner=owner, repo=name)
      repo["languages"] = api.repos.list_languages(owner=owner, repo=name)
      
      doc = {
        '_index': 'github',
        '_type': "repository", 
        '_id': f"{owner}_-_{name}",
        **repo
      }

      yield doc


if __name__=="__main__":
  repo_collector()