============
dreamhostapi
============

``dreamhostapi`` is a thin wrapper for DreamHost's HTTP-based API.

Basic usage looks like this::

    from dreamhostapi import DreamHostAPI
    api = DreamHostAPI('MY_API_KEY')
    api.dns.list_records()

More details can be found on the `project page`_.

.. _project page: http://github.com/mcgid/python-dreamhostapi


