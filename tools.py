import logging
from duckduckgo_search import DDGS

logging.basicConfig(
    level=logging.INFO,
    format="%(module)s - %(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s",
    filename="career_coach_log.log",
)


class DuckDuckGoTools:
    """
    A utility class for performing web searches using the DuckDuckGo search engine.

    This class provides methods to query the web and retrieve search results in a structured format.
    It is designed to be used as a tool by agents or other components of the application to fetch external data.

    Attributes:
        None

    Methods:
        search_web(query, num_results): Searches the web using DuckDuckGo and returns a list of results.
    """

    def search_web(self, query: str, num_results: int = 5) -> list:
        """
        Searches the web using DuckDuckGo and retrieves a specified number of results.

        This method queries DuckDuckGo with the given search term and formats the results into a list of dictionaries.
        Each dictionary contains the title, snippet (description), and link of a search result.

        Parameters:
            query (str): The search term or question to query on DuckDuckGo.
            num_results (int): The maximum number of results to retrieve (default is 5).

        Returns:
            list: A list of dictionaries, where each dictionary contains:
                - "title": The title of the search result.
                - "snippet": A brief description of the search result.
                - "link": The URL of the search result.
        """
        logging.debug(f"Searching for '{query}' with DuckDuckGo...")
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
        logging.debug(f"Found {len(results)} results for '{query}'")
        return [
            {"title": r["title"], "snippet": r["body"], "link": r["link"]}
            for r in results
        ]
