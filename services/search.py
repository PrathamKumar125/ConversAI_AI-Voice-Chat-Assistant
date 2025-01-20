# import logging
# from typing import List, Dict

# import requests
# from bs4 import BeautifulSoup
# from urllib3.exceptions import InsecureRequestWarning

# # Disable SSL warnings for requests
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# logger = logging.getLogger(__name__)

# class WebSearcher:
#     def __init__(self):
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0"
#         }
        
#     def extract_text(self, html_content: str) -> str:
#         soup = BeautifulSoup(html_content, 'html.parser')
#         # Remove unwanted elements
#         for element in soup(['script', 'style', 'nav', 'header', 'footer', 'iframe']):
#             element.decompose()
#         text = ' '.join(soup.stripped_strings)
#         return text[:8000]  # Limit text length

#     def search(self, query: str, max_results: int = 3) -> List[Dict]:
#         results = []
#         try:
#             with requests.Session() as session:
#                 # Google search parameters
#                 search_url = "https://www.google.com/search"
#                 params = {
#                     "q": query,
#                     "num": max_results,
#                     "hl": "en"
#                 }
                
#                 response = session.get(
#                     search_url,
#                     headers=self.headers,
#                     params=params,
#                     timeout=10,
#                     verify=False
#                 )
#                 response.raise_for_status()
                
#                 # Parse search results
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 search_results = soup.select('div.g')
                
#                 for result in search_results[:max_results]:
#                     link = result.find('a')
#                     if not link:
#                         continue
                        
#                     url = link.get('href', '')
#                     if not url.startswith('http'):
#                         continue
                        
#                     try:
#                         # Fetch webpage content
#                         page_response = session.get(
#                             url,
#                             headers=self.headers,
#                             timeout=5,
#                             verify=False
#                         )
#                         page_response.raise_for_status()
                        
#                         content = self.extract_text(page_response.text)
#                         results.append({
#                             "url": url,
#                             "content": content
#                         })
#                         logger.info(f"Successfully fetched content from {url}")
                        
#                     except Exception as e:
#                         logger.warning(f"Failed to fetch {url}: {str(e)}")
#                         continue
                        
#         except Exception as e:
#             logger.error(f"Search failed: {str(e)}")
            
#         return results[:max_results]




import logging
from typing import List, Dict
from transformers.agents import DuckDuckGoSearchTool

logger = logging.getLogger(__name__)

class WebSearcher:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchTool()
    
    def search(self, query: str) -> List[Dict]:
        try:
            # Execute search
            search_results = self.search_tool(query)
            
            # Convert list to string if necessary
            if isinstance(search_results, list):
                search_results = ' '.join(str(result) for result in search_results)
            
            results = [{
                "url": "duckduckgo_search",
                "content": str(search_results) # Limit content length and ensure string
            }]
            
            return results
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

# Initialize searcher
searcher = WebSearcher()