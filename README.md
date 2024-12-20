# Campbell

Python library used to interface with Campbell CR1000X dataloggers using their HTTP API interface.

[Campbell API documentation](https://help.campbellsci.com/crbasic/cr1000x/Content/Info/webserverapicommands1.htm)

This Python library is intended to mimic the structure of the Campbell API documentation.

## Installation

To install the library, you can use `pip`:

```sh
pip install campbell
```

## Usage

To use the `Campbell` library, you need to initialize the `Campbell` class with the address of the data logger and a list of tables you want to interact with.

```python
from campbell import Campbell

# Initialize the Campbell class
myCampbell = Campbell(
    address="172.17.204.40",
    tables=["myTable1", "myTable2", "myTable3"],    # Optional, will find all table if not specified
    timeout=5.22432,                                # Optional, seconds for HTML request timeout
    username="your_username",                       # Optional
    password="your_password"                        # Optional
)
```

`tables` will automatically populate a list of all available tables using the `get_tables` function

`timeout` defaults to 10 seconds if not specified

`username` and `password` is required if the datalogger has security enabled on the user's account.
Otherwise it can be omitted.

### Get Tables

The `get_tables` function retrieves a list of all available tables on the logger.

```python
myCambell.get_tables()
```


### Data Access

The `DataAccess` inner class provides methods to query data from the data logger.

The `DataAccess` class is aliased to `Data`:

```python
myCampbell.DataAccess.browsesymbols()
```

is the same as:

```python
myCampbell.Data.browsesymbols()
```

#### Data Query

The `dataquery()` function provides a way to query data from the logger.

`dataquery()` is aliased to `query()`

required keyword arguments:

- `mode`
    - The dataquery mode for accessing data
    - valid modes: 
        - `most-recent`
        - `since-time`
        - `since-record`
        - `date-range`
        - `backfill`

optional keyword arguments:

- `format`
    - The format of the returned data
    - valid formats:
        - `json`
            - wiil default to `json` if format isn't specified
            - returns a dictionary object
        - `html`
            - returns a `str`
        - `toa5`
            - returns a `str`
        - `tob1`
            - returns a `str`
        - `xml`
            - returns a `str`
- `table`
    - The data table on the logger to query
    - Will query all tables if `table` isn't specified
- `field`
    - The field withing a table to query
    - `table` must be specified

##### Most Recent

This mode returns the number of most recent records.

mode: `most-recent`

required keyword arguments:

- `records`
    - `int`
    - number of most recent records

example:
```python
myCampbell.DataAccess.dataquery(mode="most-recent", records=5)
```

returns the 5 most recent records

##### Since Time

This mode returns all the records available since the specified time.

mode: `since-time`

required keyword arguments:

- `time`
    - `datetime.datetime`
    - the specified time

example:
```python
import datetime

myCampbell.Data.query(mode="since-time", time=datetime.datetime(2024,12,19,16,30,5))
```
returns all the records since 2024-12-19 16:30:05

##### Since Record

This mode returns all the records since a specified record number.

mode: `since-record`

required keyword arguments:

- `record`
    - `int`
    - the specified record

example:
```python
myCampbell.Data.query(mode="since-record", record=785631)
```
returns all the records since record number 785631

##### Date Range

This mode returns all the records between a specified date range

mode: `date-range`

required keyword arguments:

- `start`
    - `datetime.datetime`
    - the start of the date range
- `end`
    - `datetime.datetime`
    - the end of the date range

example:
```python
import datetime

myCampbell.Data.query(mode="date-range",
                      start=datetime.datetime(2024,6,1,0,5,0),
                      end=datetime.datetime(2024,6,2,10,5,3))
```
returns all the records between 2024-06-01 00:05:00 and 2024-06-02 10:05:03

##### Backfill

This mode returns all the records during a specified previous amount of time

mode: `backfill`

required keyword arguments:

- `interval`
    - `datetime.timedelta`
    - the ammount of time

example:
```python
import datetime

myCampbell.Data.query(mode="backfill", interval=datetime.timedelta(minutes=35))
```
returns all the records logged in the past 35 minutes

#### Browse Symbols

Returns all the available symbols in the logger.

optional keyword arguments:

- `format`
    - The format of the returned data
    - valid formats:
        - `json`
            - wiil default to `json` if format isn't specified
            - returns a dictionary object
        - `html`
            - returns a `str`
        - `xml`
            - returns a `str`
- `table`
    - The data table on the logger to query
    - Will query all tables if `table` isn't specified

example
```python
myCampbell.Data.browsesymbols()
```
returns all the available data tables on the logger

### Control Commands

The `ControlCommand` inner class provides methods to query data from the data logger.

The `ControlCommand` class is aliased to `Control`:

```python
myCampbell.ControlCommand.clockcheck()
```

is the same as:

```python
myCampbell.Control.clockcheck()
```

#### Set Value X

#### Clock Check

#### Clock Set

### File Management

The `FileManagement` inner class provides methods to query data from the data logger.

The `FileManagement` class is aliased to `File`:

```python
myCampbell.FileManagement.addfile()
```

is the same as:

```python
myCampbell.File.addfile()
```

#### Newest File

This function is not yet implemented

#### List Files

This function is not yet implemented

#### File Control

This function is not yet implemented

#### Add File

This function is untested

required arguement:

- `filename`
    - `str`
    - the filename/path to the file you want to add

example:
```python
myCampbell.File.addfile('test.txt')
```

Returns the result codes. Result code descriptions are provided in the API documentation.