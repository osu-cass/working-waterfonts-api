Draft API
=========

Format
------

Responses will be returned in standard JSON format. An attempt will be made to keep the structure simple. Https will be used for all endpoints. 

Null values (optional fields that do not have data), will be empty strings: "".

Versions
--------

The API will be versioned with simple version integers, 1, 2, 3, ...

ex: https://working-waterfronts.org/1/pois

Errors
------

Error records will be returned in every message, and will consist of a dictionary containing the error status, error name, error text and error level. The status field will indicate the presence of an error condition, and should be checked before attempting to process the rest of the response.

example:

.. code-block:: json

	error: {error_status: true, error_name: 'not_found_error', error_text: 'poi with id=232 could not be found', error_level: 10}

Extended Fields
---------------

To allow for future expandability, a dictionary call 'ext' will be included with every response. This dictionary will either contain no records, or will contain additional first-class records that were not included in the original specification. For instance, if a new attribute "color" is later added to the product response, it can be included in the extended attributes array. Applications can choose to discover/use these new fields or ignore them without effecting backwards compatibility. Response validation should include the presence of ext, but not its contents.


Endpoints
---------

*/pois*

Return a dictionary containing a record for every poi in the database. This data is unlikely to change frequently, it should be in long-term storage on the device and refreshed periodically.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
	        pois:  [
            {id: int,
			name: text,
			alt_name: text or null,
			summary: text,
            lat: float,
            long: float,
            street: varchar,
            city: varchar,
            state: varchar,
            zip: varchar,
            description: text
            location_description: text,
            history: text,
            facts: text,
            contact_name: varchar,
            phone: varchar,
            website: url,
            email: email,
			created: datetime,
			modified: datetime,
			ext: {attribute: value, attribute: value...} or {}},
		    {...},
		    {...}
            ]
	}


*/pois/<id>*

Returns a single poi record identified by <id>. This will return all available details about a poi.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
            id: int, 
			name: text,
			alt_name: text or null,
			summary: text,
            lat: float,
            long: float,
            street: varchar,
            city: varchar,
            state: varchar,
            zip: varchar,
	        description: text,
            history: text,
            facts: text,
            location_description: text (optional),
            contact_name: varchar,
            phone: varchar (optional),
            website: url (optional),
            email: email (optional),
            categories: [category1, category2, ...]
            videos: {description1: link1, description2: link2,...}
            images: {caption1: link1, caption2: link2,...}
			created: datetime,
			modified: datetime,
			ext: {attribute: value, attribute: value...} or {},
	}
	

*/pois/categories/<id>*

Returns a list of pois in the category identified by <id>.

.. code-block:: json

	{
		error: {error_status: bool, error_name: text, error_text: text, error_level},
	        pois:  [
            {id: int,
			name: text,
			alt_name: text or null,
			summary: text,
            lat: float,
            long: float,
            street: varchar,
            city: varchar,
            state: varchar,
            zip: varchar,
			created: datetime,
			modified: datetime,
			ext: {attribute: value, attribute: value...} or {}},
		    {...},
		    {...}
            ]
	}

    
Additional parameters
---------------------

These parameters can be added to any endpoint request

*?location=<lat>,<long>*

or 

*?lat=<float>&long=<float>*

These parameters represent the latitude and longitude of either the mobile device’s current location, or a pre-defined location such as “Newport, OR”. These will cause the results to be sorted by proximity, closest items first. This parameter will be ignored with the /stories endpoint. Depending on how the device handles the coordinates, it may be more convenient to send a single parameter, ‘location=<lat>,<long>’ and use the latitude and longitude as positional arguments.

examples:

.. raw:: html

	https://working-waterfronts.org/pois?lat=49.28472&long=89.7982
	https://working-waterfronts.org/pois?location=49.28472,89.7982


*?limit=<int>*

This parameter will limit the number of records returned to <int>. In combination with the location parameter, it can be used to return the 5 nearest vendors selling tuna:

.. raw:: html

	https://working-waterfronts.org/pois/<poi_id>?lat=49.28472&long=89.7982&limit=10

*?proximity=<int>*

This parameter will restrict the returned results to those within <int> miles (or configurable distance unit) of the given location. Ignored if no location is given.
