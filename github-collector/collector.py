"""
Module used for collecting repository metadata from GitHub
"""
import os
import asyncio
from time import sleep
from ghapi.all import GhApi
from ghapi.page import paged
from dotenv import load_dotenv

load_dotenv( override=True )

# Load credentials from .env file
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

api = GhApi(token=GITHUB_TOKEN)

def api_searcher(query: str) -> dict:
  """Searches for documents that match query string"""
  repos = paged(api.search.repos, per_page=100, q=query)

  for repo in repos:
    # corrosponds to 10 request per min limit of search API
    sleep(7)
    yield repo['items']


async def repo_collector(query: str = "q=OpenSearch") -> dict:
  """Yields OpenSearch formatted documents that match the query"""
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
