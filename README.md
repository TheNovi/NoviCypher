# NoviCypher
For information about cipher read [wiki on github](https://github.com/TheNovi/NoviCypher/wiki).

## How to use API.py
Run it and follow instructions

### Parameters
#### Encode
`> API.py Path Rows Size`
* Path must be a folder (not a file).
* Rows is a number of rows (20 - 50 recommended).
* Size is a number of columns (100 - 1000 recommended).
* Next API is going to ask you for the key.

Example:
`> API.py C:/Example/ToEncode 20 500`

#### Decode
`> API.py Path`
* Path must be `.ncy` file (nothing else is going to work).
* Next API is going to ask you for a key.

Example:
`> API.py C:/Example/ToDecode.ncy`
