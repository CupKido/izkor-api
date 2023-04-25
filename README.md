# Izkor REST API

An api that supplies info about fallen israeli soldiers/citizens in past wars and terror attacks.

The API uses the government website as a source of information, and extract the data it needs from it.

Feel free to use the server/wrapper for any of your needs, as long as it respects the fallen soldiers and their families.

### Usage:
run -

    python main.py -p <port to use>

The default port is 3500.

The server currently only has support for http.

### Available endpoints:

#### /GetHalalimByName
##### parameters
* first_name - first name
* last_name - last name

returns a list of Halalim that match the parameters.

every element in the list includes:

* id
* first_name
* last_name
* father (name)
* mother (name)
* year_of_fall
* beit_kvarot (which cemetery)
* cheil (which force)
