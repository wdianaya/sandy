import requests


API_KEY = 'AIzaSyA8N6s4UOI_Z4qt04mLICAUltanrljAA4A'
query = "python"
# using the first page
page = 1
# constructing the URL
# doc: https://developers.google.com/custom-search/v1/using_rest
# calculating start, (page=2) => (start=11), (page=3) => (start=21)
start = (page - 1) * 10 + 1
url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"