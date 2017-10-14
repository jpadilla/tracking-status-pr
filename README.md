# Tracking status.pr

This tool scrapes status.pr every hour and keeps tracks of changing metrics in order to help visualize and measure progress. Data is also made available in CSV and JSON formats.

## Running

### Web

```
$ MONGODB_URI='mongodb://localhost/tracking-status-pr' FLASK_DEBUG=1 FLASK_APP=app/app.py flask run
```

### Scraper

```
$ MONGODB_URI='mongodb://localhost/tracking-status-pr' python scraper.py
```
