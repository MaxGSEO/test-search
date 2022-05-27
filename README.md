### Install packages.
Create virtualenv first and then install poetry.

I added you to the Topical Authority builder repo for the new Search entities extraction and topic modeling

it has a left sidebar and the main part as the previous one. it has a different Lotti logo (I'll sed you the code for its data file) and the same header

On the left sidebar, the thing you need for now is a dropdown menu with a "Select Search API" title and the possibility to choose between DataForSEO or scaleSERP.

Send me you email, and I'll invite you to the DataForSEO dashboard.

Credential for Scaleserp (to provide a service with a free daily quota too)


https://app.scaleserp.com/
geraci.massimiliano@gmail.com
dp0Uh0B1NwDT

The Search part of the search UI is something like the attached pic

### Razor api for testing
```text
f0852f0515c92c0686d129f79ff9c5584b87c1b67d503073a4c93ec9
```

Test urls
```text
https://alimentazionebambini.e-coop.it/pedagogia/giochi-di-natale-con-i-numeri-idea-montessori-5-6-anni/
https://alimentazionebambini.e-coop.it/pedagogia/metodo-montessori/ciclo-vitale-di-una-piantina-per-bambini-piccoli/
```

POST: https://api.dataforseo.com/v3/serp/google/organic/live/advanced

[
    {
        "language_name": "English (United Kingdom)",
        "location_name": "London,England,United Kingdom",
        "keyword": "brexit",
        "search_param":"tbm=nws"
    }
]