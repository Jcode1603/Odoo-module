import xmlrpc.client

url = 'http://20.102.80.13:8069'
db = 'Odoo14'
username = 'dipo.jaji@panoramicsynergy.co.uk'
password = 'Official@123'


# info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
# url, db, username, password = info['host'], info['database'], info['user'], info['password']
# print(url)

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(common.version())

uid = common.authenticate(db, username, password, {})



# 1. The second endpoint is xmlrpc/2/object. It is used to call methods of odoo models via the execute_kw RPC function. Each call to execute_kw takes the following parameters:

# the database to use, a string the user id (retrieved through authenticate), an integer

# the user’s password, a string the model name, a string

# the method name, a string an array/list of parameters passed by position, a mapping/dict of parameters to pass by keyword (optional)

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})


# 2. List records
# Records can be listed and filtered via search().

# search() takes a mandatory domain filter (possibly empty), and returns the database identifiers of all records matching the filter.
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]])
#print(models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]]))
# 2b. By default a search will return the ids of all records matching the condition, which may be a huge number. 
# offset and limit parameters are available to only retrieve a subset of all matched records.
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'offset': 10, 'limit': 5})


# 3. Count records
# Rather than retrieve a possibly gigantic list of records and count them, search_count() can be used to retrieve only the number of records matching the query. 
# It takes the same domain filter as search() and no other parameter.
models.execute_kw(db, uid, password, 'res.partner', 'search_count', [[['is_company', '=', True]]])


# 4. Read records
# Record data are accessible via the read() method, which takes a list of ids (as returned by search()), 
# and optionally a list of fields to fetch. By default, it fetches all the fields the current user can read, which tends to be a huge amount.
ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True]]], {'limit': 1})
[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
# count the number of fields fetched by default
len(record)
# Conversely, picking only three fields deemed interesting.
models.execute_kw(db, uid, password, 'res.partner', 'read', [ids], {'fields': ['name', 'country_id', 'comment']})


# 5. List record fields
# fields_get() can be used to inspect a model’s fields and check which ones seem to be of interest.

# Because it returns a large amount of meta-information (it is also used by client programs) it should be filtered before printing, 
# the most interesting items for a human user are string (the field’s label), 
# help (a help text if available) and type (to know which values to expect, or to send when updating a record).
models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})


# 6. Search and read
# Because it is a very common task, Odoo provides a search_read() shortcut which, as its name suggests, 
# is equivalent to a search() followed by a read(), but avoids having to perform two requests and keep ids around.

# Its arguments are similar to search()’s, but it can also take a list of fields (like read(), if that list is not provided it will fetch all fields of matched records).
models.execute_kw(db, uid, password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['name', 'country_id', 'comment'], 'limit': 5})


# 7. Create records
# Records of a model are created using create(). The method creates a single record and returns its database identifier.

#create() takes a mapping of fields to values, used to initialize the record. For any field which has a default value and is not set through the mapping argument, 
# the default value will be used.
id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner"}])


# 8. Update records
# Records can be updated using write(). It takes a list of records to update and a mapping of updated fields to values similar to create().

# Multiple records can be updated simultaneously, but they will all get the same values for the fields being set. 
# It is not possible to perform “computed” updates (where the value being set depends on an existing value of a record).
models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'name': "Newer partner"}])
# get record name after having changed it
models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])


# 9. Delete records
# Records can be deleted in bulk by providing their ids to unlink()
models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
# check if the deleted record is still in the database
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['id', '=', id]]])

# Inspection and introspection
# While we previously used fields_get() to query a model and have been using an arbitrary model from the start, 
# Odoo stores most model metadata inside a few meta-models which allow both querying the system and altering models and fields (with some limitations) on the fly over XML-RPC.


