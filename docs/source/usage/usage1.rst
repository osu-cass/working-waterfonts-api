.. _usage:

Usage
=====

The Working Waterfronts API web app is used to enter the data that is 
displayed in the Working Waterfronts Mobile app. It consists of a series of 
simple forms for each type of object that can be added to the database. 
Required fields are marked with a *, and any errors or missing items will be 
flagged when the form is saved. The data will not be saved until errors are 
corrected.

Objects
-------

There are five major objects in Working Waterfronts: Points of Interest,
 Categories, Hazards, Videos and Images. When you log in to the application, 
 the first screen you see is the Entry screen, which lists the objects. 
 Clicking on one of the object buttons will bring you to a screen listing all 
 of the objects already saved in the system.

For example, clicking Points of Interest will display a table listing all the 
Points of Interest currently in the system. On this screen you can add a new 
Point of Interest by clicking the yellow "New Vendor" button at the top of the 
list, or edit any of the existing Points of Interest by clicking on that Point
of Interest.


Adding and Editing
------------------

The forms for editing and for adding new objects are the same, except that the 
edit form will already be filled out with the existing data. You can edit this 
data and save the changes using the "Save" button at the bottom of the form, or
 delete the entire record using the red "Delete" button on the top of the form.

Workflow
++++++++

While the objects in Working Waterfronts don't depend on each other, they are
connected. For example, a Point of Interest may need a Category, Hazard, and images. We recommend the following work flows to add different objects:

**Products**

1.	Determine what Preparations are available for this Product (smoked, dried, fresh, etc).
2.	Create the Preparation objects if they don't already exist.
3.	If there is an Image for this Product, create an Image object (be sure to give the image a unique and descriptive name).
4.	If this Product has a Story, make sure that Story exists (for instance, the Salmon story will probably be shared by all varieties of Salmon).
5.	Create the Product object, selecting the correct Story and Image, and add each applicable preparation.

**Vendors**

1.	Make sure this Vendor's Products are added (see above).
2.	If the Vendor has a Story (rare), create the Story object.
3.	Create the Vendor object, adding the correct Products and selecting a Story, if applicable.

**Stories**

1.	If this Story includes Images, create the Images.
2.	If this Story includes Videos, create the Videos.
3.	Create the Story object, adding the correct Images and Videos, if applicable.

See below for details on adding these objects.

Points of Interest
++++++++++++++++++

These are the records of **something**. 

**Required Data**

Certain information is required to create a new Point of Interest, make sure you know these items before starting:

*Name*
	The name of the Point of Interest.
*Description*
	A brief description of the Point of Interest.
*History*
    A summery of the Point of Interest's history.
*Facts*
    Any interesting facts about the Point of Interest.
*Address*
	The street address where the products are being sold.
		* Street Address
		* City
		* State
		* Zipcode
*Contact Name*
	The primary contact name for this Point of Interest.

.. note::
	
	Street addresses are turned into GPS coordinates for display on a map in the Mobile app, so it is important to be accurate.


**Optional Data**

Additionally, there are several optional fields:

*Alt Name*
    An alternate name for the Point of Interest. 
*Location Description*
	Additional details about how to find the Point of Interest's location (**Insert
    example here**).
*Website*
	The Point of Interest's website.
*Email*
	The Point of Interest's primary email address.
*Phone*
	The Point of Interest's phone number.
*Images*
    Any images of the Point of Interest.
*Videos*
    Any videos of the Point of Interest.
*Hazards*
    Any hazards in or around the Point of Interest. (Such as heights, falling
    rocks, hard hats required, etc.)
*Categories*
    The type of Point of Interest.


Category
++++++++

Categories are the types of Points of Interest. **some examples**

**Required Data**

Categories require the following fields to be filled out:

*Category*
    The name of the category.

**Optional Data**

Categories have no optional fields.

Hazards
+++++++

Hazards are dangers that may be found at a Point of Interest.

**Required Data**

Hazards require the following fields to be filled out:

*Name*
	The name of the Hazard.
*Description*
	A brief description of the Hazard.

**Optional Data**

Hazards have no optional fields.

Videos
++++++

Videos are external links to videos hosted on YouTube, Vimeo, or elsewhere. Any video that can be streamed can be used here.

**Pre-requisites**

Videos have no pre-requisites.

**Required Data**

Videos require the following fields to be filled out:

*Name*
	A name for this Video. (This should be unique and easy to identify from the Video pull-down menu on the Point of Interest form.)
*Link*
	The URL for this video (ex. https://www.youtube.com/watch?v=hl3wWwouOUE).
*Caption*
	A brief descriptive caption for this Video.

**Optional Data**

Videos have no optional fields.


Images
++++++

Images are uploaded image files. The Image upload form accepts .jpg, .png, and .gif image files. 

**Pre-requisites**

Images have no pre-requisites.

**Required Data**

Images require the following fields to be filled out:

*Image*
	Upload an image file.
*Name*
	A name for this Image. (This should be unique and easy to identify from the Image pull-down menu on the Point of Interest form.)
*Caption*
	A brief descriptive caption for this Image.

**Optional Data**

Images have no optional fields.
