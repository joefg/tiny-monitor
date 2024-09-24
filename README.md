# tiny monitor

A service monitor in one Python script.

Just pings a web page and reports whether it's alive or not.

## Known issues

Some web hosts block plain `urllib.request.urlopen` because it looks
like a web scraper, so you might have `403 Forbidden` or similar appear.

This isn't an issue for me because I use this to monitor self-hosted stuff
on my home network. For monitoring real projects, there are better cloud-hosted
services out there.

## How to use

Create your config.json (here's mine):

```json
{
    "services": [
        {
            "name": "google.com",
            "url": "http://google.com"
        },
        {
            "name": "nginx",
            "url": "http://localhost:80"
        }
    ]
}
```

Add the following to your server's crontab:

```crontab
* * * * 30 python3 /path/to/tinymonitor.py -c /path/to/config.json > /var/www/html/index.html
```

No `venv`, no `dockerfile`, uses entirely system Python.
