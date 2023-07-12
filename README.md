## Short Info

- Application is a Fast Api webservice parsing articles as a background job every minute.
- scrapers for 2 websites are defined - www.sme.sk, www.hn.cz
- articles (url, header, keyword) are inserted to db and then cached - as 1 minute is not a long interval for change of
  news portal
  the cache is always checked and only if any new articles are scraped, the insert to db is made
- db contains 2 tables - articles and keywords connected via url
- warning: FOR NOW, DB CONNECTION IS HARDCODED IN app.py -> for full functionality, application needs postgres db
  called "news" running on port
  5432, otherwise only cache is used and endpoint calls do not work

## Missing (not implemented yet)

- application (both webservice and db) is not dockerized yet
- unit tests are not written
- db connection is hard coded in app.py
- more robust db error handling (f.e. in case db connection is lost after engine creation)

## Bugs

- before 1st api call, parser needs to run at least once

## Extension ideas (ordered by importance)

- add user management to database handler
- semantic search of keywords (e.g. "ukrajina" should also find "ukrajinec"), using word2vec or some transformer model
- keyword typos correction (e.g. "ukrajina" should also find "ukrajna") - compare query with existing keywords and if
  similarity is high, use the existing keyword
- add user management to webservice
- simple GUI for data querying

## Requirements:

- Python 3.10+, `pip`
- list of reqs in requirements.txt

## Example run:

```
uvicorn --host 0.0.0.0 --port 8080 --workers 1 rest_api.app:app 
```

## Testing the REST API:

```bash
curl -X GET -H "Content-Type: application/json" -d '{"keywords": ["TEST", "ukrajina"]}' http://0.0.0.0:8080/articles/find 
```