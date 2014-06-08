# dreamhostapi

## Usage

#### DreamHost [Has An API](dhwiki-api)

It is HTTP-based:

```bash
$ curl 'https://api.dreamhost.com/?key=AN_API_KEY&unique_id=1234567&cmd=dns-list_records'
```

That's not very Pythonic.


#### `dreamhostapi` Is A Wrapper

```python
>>> from dreamhostapi import DreamHostAPI
>>> api = DreamHostAPI('MY_API_KEY')
>>> api.dns.list_records()
```

That's more Pythonic.


#### Calling `dir()` On It Is Not Very Helpful

```python
>>> dir(api)
['API_URL', '__class__', '__delattr__', '__dict__', '__doc__', '__format__',
'__getattr__', '__getattribute__', '__hash__', '__init__', '__module__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
'__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_call', 'key']
```

It doesn't know whether an API command (method) exists until you try to use it.

(On the bright side, if DreamHost adds a new API command you can just call it,
without `dreamhostapi` needing to be updated.)


#### But There's an Interactive Version

```python
>>> from dreamhostapi import InteractiveAPI
>>> api = InteractiveAPI('MY_API_KEY')
>>> dir(api)
['account', 'announcement_list', 'api', 'dns', 'domain', 'dreamhost_ps',
'jabber', 'mail', 'mysql', 'oneclick', 'rewards', 'services', 'user']
>>> dir(api.dns)
['add_record', 'list_records', 'remove_record']
```

It finds out which API commands are available when you create it. Doing that
work when you don't intend to `dir()` it would be a waste, so that's in this
class instead of the main `DreamHostAPI` class.

If the method you're calling doesn't actually exist in the API, it will raise
an `AttributeError`.


## Details

#### Keys

To use the API, you need an API key. It's a string of letters and numbers. You
create one in the Web Panel API section of DreamHost's Web Panel. (Just go to
the Panel and search for "API".) It lets you select which API commands the key
will be able to use.

You supply the API key as the parameter when creating a `DreamHostAPI` or
`InteractiveAPI` object:

```python
>>> from dreamhost import DreamHostAPI
>>> api = DreamHostAPI('THE_API_KEY_GOES_HERE')
```

#### Commands

DreamHost has organized related API commands into API "modules": dns, account,
etc.

API modules map to attributes on the `DreamHostAPI` object: `api.dns`,
`api.account`, etc.

The various commands are methods of those module attributes:
`api.dns.list_records()`, `api.dns.add_record(...)`, etc.

If a command needs arguments, like `api.dns.add_record(...)`, you must supply
them as **named** parameters to the method:

```python
>>> api.dns.add_record(record='example.com', type='A', value='1.2.3.4')
```

The required and optional arguments for most commands are listed [in DreamHost's
wiki](dhwiki-api). (Why just "most"? See **Problems** below.)

#### Returned Data

All returned data are Unicode strings, usually in a `list` or a `dict` or a
combination of the two.


#### Errors

If an API command fails, it will raise an `APIError`:

```python
>>> api.dns.add_record()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "dreamhostapi/module.py", line 31, in method
    raise APIError(response['data'])
dreamhostapi.exceptions.APIError: no_record
```

If the command you're calling doesn't actually exist in the API, an
`AttributeError` will be raised.

If you try to call a command that the current API key doesn't have permission
to use, you'll get an `APIError` with the message
`this_key_cannot_access_this_cmd`:

```python
>>> api = API('DNS_ONLY_KEY')
>>> api.account.list_accounts()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "dreamhostapi/module.py", line 31, in method
    raise APIError(response['data'])
dreamhostapi.exceptions.APIError: this_key_cannot_access_this_cmd
```

This is true even if the command doesn't exist:

```python
>>> api = API('DNS_ONLY_KEY')
>>> api.account.foobar()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "dreamhostapi/module.py", line 31, in method
    raise APIError(response['data'])
dreamhostapi.exceptions.APIError: this_key_cannot_access_this_cmd
```

This doesn't raise an `AttributeError` because the API key doesn't have access
to the `account` API module commands — the permission error supercedes the
command-doesn't-exist error.


## Problems

DreamHost's wiki doesn't currently (2014-06-08) have any information about
these API commands:

- `account-list_accounts`
- `domain-list_certificates`
- `dreamhost_ps-add_key`
- `dreamhost_ps-list_keys`
- `dreamhost_ps-remove_key`
- `oneclick-catalog`
- `oneclick-describe_app`
- `oneclick-destroy_custom`
- `oneclick-install_custom`
- `oneclick-list_custom`
- `oneclick-update`
- `oneclick-update_all`
- `user-list_users_no_pw`

This makes it trickier to know how to use these commands. Try using
`api.api.list_accessible_cmds()` to get a bit more information.

Unfortunately, though `list_accessible_cmds()` has the ability to communicate some
pretty useful information—required and optional arguments, and name/order of
returned data—it currently doesn't actually do much of that. In many places, it
just says `see_docs`.


[dhwiki-api]: http://wiki.dreamhost.com/API
