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
    tables=["myTable1", "myTable2", "myTable3"],
    timeout=5.22432,           # Optional, seconds for HTML request timeout
    username="your_username",  # Optional
    password="your_password"   # Optional
)
```

### Data Access

The `DataAccess` class provides methods to query data from the data logger.

required keyword arguments:

- mode
    - The dataquery mode for accessing data
    - valid modes: 
        - `most-recent`
        - `since-time`
        - `since-record`
        - `date-range`
        - `backfill`

#### Most Recent

This mode user-specified number of most recent records.

mode: `most-recent`

required keyword arguments:

- records
    - number of most recent records (int)

example:
```python
myCampbell.DataAccess.dataquery(mode="most-recent", records=5)
```

This will print the 5 most recent records

#### Since Time