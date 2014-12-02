Draft Data model
================

pois
----

.. code-block:: python

	id                      int (pk)
	name                    varchar
	alt_name                varchar (optional)
	summary                 text
	lat                     float
	long                    float
	street                  varchar
	city                    varchar
	state                   varchar
	zip                     varchar
	description             text
	location_description    text (optional)
    history                 text
    facts                   text
	contact_name            varchar
	phone                   varchar (optional)
	website                 url (optional)
	email                   email (optional)
	created                 datetime
	modified                datetime (auto-update on modification)


categories
----------

.. code-block:: python

	id          int (pk)
	category    varchar


images
------

.. code-block:: python

	id          int (pk)
    name        varchar
    poi_id      int (foreign key to poi)
	image       image (file)
	caption     text (optional)
	created     datetime
	updated     datetime (auto-update on modification)

videos
------

.. code-block:: python

	id              int (pk)
    name            varchar
    poi_id          int (foreign key to poi)
	video           link
	description     text (optional)
	created         datetime
	updated         datetime (auto-update on modification)


hazards
-------
    
.. code-block:: python

    id              int (pk)
    name            varchar
    description     text
	created         datetime
	updated         datetime (auto-update on modification)

pois_hazards
------------

.. code-block:: python
    
    poi_id      int (foreign key to poi)
    hazard_id   int (foreign key to hazard)

pois_categories
---------------

.. code-block:: python

	poi_id          int (foreign key to poi)
	category_id     int (foreign key to category)
