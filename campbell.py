import requests


class campbell:
    """Used to interface with Campbell Scientific data loggers"""

    def __init__(self, address: str, tables: list) -> None:
        """Initializes the class with the address of the data logger and a list of tables"""
        self.address: str = address
        self.tables: list = tables
        self.datafields: dict = self._datafields()
        self.data: dict = self.pull_recent()

    def _fields(self, table) -> list:
        """Returns a list of fields for a given table"""
        command = "dataquery"
        format = "json"
        mode = "backfill"
        parameter = "p1=1"

        url = f"http://{self.address}/?command={command}&uri=dl:{table}&format={format}&mode={mode}&{parameter}"

        response = requests.get(url)

        fields: list = []

        if response.status_code == 200:
            data = response.json()
            for i in range(len(data["head"]["fields"])):
                fields.append(data["head"]["fields"][i]["name"])
        else:
            print(f"Failed to retrieve data: {response.status_code}")

        return fields

    def _datafields(self) -> dict:
        """Returns a dictionary of fields for all tables"""
        datafields: dict = {}
        for table in range(len(self.tables)):
            datafields[self.tables[table]] = self._fields(self.tables[table])
        return datafields

    def pull_recent(self) -> dict:
        """Pulls the most recent data"""

        data: dict = {}

        command = "dataquery"
        format = "json"
        mode = "backfill"
        parameter = "p1=1"

        for table in self.tables:
            url = f"http://{self.address}/?command={command}&uri=dl:{table}&format={format}&mode={mode}&{parameter}"

            response = requests.get(url)

            if response.status_code == 200:
                recent_data = response.json()
                data[table] = recent_data
            else:
                print(f"Failed to retrieve data: {response.status_code}")

        return data
