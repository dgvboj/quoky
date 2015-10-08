# Quoky

quoka scraper. Uses scrapy and sqlalchemy to crawl a site and extract information. Tested with `Python 2.7`.

# Database

I have used sqlalchemy to encapsulate database accesses, so that it is easy to change backend. First tests performed with `Sqlite`, then moved to `MySQL`. I have used the `mysql+pymysql` as driver.

# NO Javascript

No `javascript`: not possible to activate `JS` execution with pure `Scrapy`. Extra tools are needed for this (for example, `splash + scrapyjs`). This requires a much more complex setup. As a consequence, the following functionality is not yet implemented:

- not all cities are processed, only the 6 visible by default. To show all cities, a javascript function must be executed
- the selector "nur Angebote" is also JS
- the selector "Privat / Gewerblich" is also JS
- telefon numbers are not fully shown
- "Partner Anzeige" are displayed via JS, so these are also no considerered

# Data formats

- `Erstellungsdatum`: not parsed because it has a free format: "vor 6 Monaten" or "16.08.2015". This can be parsed with the help of libraries, or dropping entirely the values like "vor 6 Monaten".
- `OBID`: used `String(20)` instead of `Integer`
- `Anbieter_ID`: used `String(20)` instead of `Integer`

# Execution time

Running with an SQLite backend, 876 are generated in 1m (68 ms/entry)

```
$ time scrapy runspider quoky/spiders/quoka.py
real    1m0.258s
user    0m21.067s
sys     0m0.412s
```

Running with an MySQL backend, 876 are generated in 1m3s (72 ms/entry)

```
$ time scrapy runspider quoky/spiders/quoka.py
real    1m2.835s
user    0m16.979s
sys     0m0.433s
```
