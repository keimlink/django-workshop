Caching
*******

Bis Django 1.2 konnte nur ein Cache Backend in ``CACHE_BACKEND`` konfiguriert
werden. Seit Django 1.3 gibt es ``CACHES``, wo man mehrere Cache Backends
konfigurieren kann.

Cache Backends
==============

Als Cache Backends stehen zur Verfügung:

- :djangodocs:`Memcached <topics/cache/#memcached>`
- :djangodocs:`Datenbank <topics/cache/#database-caching>`
- :djangodocs:`Dateisystem <topics/cache/#filesystem-caching>`
- :djangodocs:`Local-Memory <topics/cache/#local-memory-caching>`
- :djangodocs:`Dummy Caching (zur Entwicklung) <topics/cache/#dummy-caching-for-development>`

Jedes Cache Backend kann mit
:djangodocs:`Optionen <topics/cache/#cache-arguments>` konfiguriert werden::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }

Anwendungsmöglichkeiten der Caches
==================================

Es gibt verschiedene Möglichkeiten zu Cachen:

- Die :djangodocs:`ganze Website <topics/cache/#the-per-site-cache>` mit Hilfe von Middleware cachen
- :djangodocs:`Einzelne Views <topics/cache/#the-per-view-cache>` mit Hilfe von Dekoratoren cachen (in :file:`views.py` oder :file:`urls.py`)
- Einzelne :djangodocs:`Templateteile cachen <topics/cache/#template-fragment-caching>`

Mit der :djangodocs:`Cache API <topics/cache/#the-low-level-cache-api>` kann
man spezielle Caching Probleme lösen::

    >>> from django.core.cache import cache
    >>> cache.set('my_key', 'hello, world!', 30)
    >>> cache.get('my_key')
    'hello, world!'
    # Wait 30 seconds for 'my_key' to expire...
    >>> cache.get('my_key')
    None

Mit Hilfe von ``KEY_PREFIX`` kann man einen :djangodocs:`Prefix für
verschiedene Caches konfigurieren <topics/cache/#cache-key-prefixing>`, damit
diese getrennt sind.

``VERSION`` :djangodocs:`versioniert den Cache <topics/cache/#cache-versioning>`
und man kann einfach Teile des Caches löschen.

Außerdem kann man Dekoratoren nutzen, um entweder :djangodocs:`HTTP Header als
Cache-Kriterien zu nutzen <topics/cache/#using-vary-headers>` oder um
:djangodocs:`HTTP Header zu senden <topics/cache/#controlling-cache-using-other-headers>`,
die sich auf das Caching beziehen.
