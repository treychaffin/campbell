import requests
import datetime
import base64
import time
from typing import Union
from urllib.parse import quote
import logging

log = logging.getLogger(__name__)


class Campbell:
    """
    Used to interface with Campbell Scientific data loggers via the web API

    https://help.campbellsci.com/crbasic/cr1000x/Content/Info/webserverapicommands1.htm
    """

    def __init__(self, address: str, **kwargs) -> None:
        """
        Initializes the class with the address of the data logger
        and a list of tables
        """

        start_time = time.time()
        self.address: str = address

        self.timeout = kwargs.get("timeout", 10)
        if "username" in kwargs and "password" in kwargs:
            self.username = kwargs["username"]
            self.password = quote(kwargs["password"])

        self.DataAccess = self._DataAccess(self)
        self.Data = self.DataAccess  # alias
        self.ControlCommand = self._ControlCommand(self)
        self.Control = self.ControlCommand  # alias
        self.FileManagement = self._FileManagement(self)
        self.File = self.FileManagement  # alias

        if "tables" in kwargs:
            self.tables = kwargs["tables"]
        else:
            self.tables = self._get_tables()

        end_time = time.time()
        duration = end_time - start_time
        log.info(f"Initialization took {duration:.6f} seconds")

    def _get_tables(self) -> list:
        tables = []
        for name in self.Data.symbols()['symbols']:
            tables.append(name['name'])
        return tables

    def _api_request(self, command: str, **kwargs) -> Union[dict, str, None]:

        if "format" in kwargs:
            format = kwargs["format"]
            kwargs.pop("format")
        else:
            format = "json"

        if hasattr(self, "username") and hasattr(self, "password"):
            url = f"http://{self.username}:{self.password}@{self.address}/"
        else:
            url = f"http://{self.address}/"

        if "new_file_name" in kwargs:
            url += f"{kwargs['new_file_name']}"

        url += f"?command={command}"

        if "expr" in kwargs:
            url += f"&expr={kwargs['expr']}"

        if "file1" in kwargs:
            url += f"&file={kwargs['file1']}"

        if "file2" in kwargs:
            url += f"&file2={kwargs['file2']}"

        if "action" in kwargs:
            url += f"&action={kwargs['action']}"

        if "table" in kwargs:
            url += f"&uri=dl:{kwargs['table']}"

        if "field" in kwargs:
            url += f".{kwargs['field']}"

        if "value" in kwargs:
            url += f"&value={kwargs['value']}"

        if "mode" in kwargs:
            url += f"&mode={kwargs['mode']}"

        valid_format_commands = ["ClockSet",
                                 "ClockCheck", "dataquery", "browsesymbols"]
        if command in valid_format_commands:
            url += f"&format={format}"

        if "time" in kwargs and command == "ClockSet":
            url += f"&time={kwargs['time']}"

        if "parameter1" in kwargs:
            url += f"&p1={kwargs['parameter1']}"

        if "parameter2" in kwargs:
            url += f"&p2={kwargs['parameter2']}"

        log.debug(f"{url=}")

        response = self._request(url)
        if response.status_code == 200:
            if "format" in kwargs and kwargs["format"] == "json":
                return self._request(url).json()
            else:
                return self._request(url).text

    def _request(self, url) -> requests.Response:
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            log.error(f"Http Error: {errh}")

        except requests.exceptions.ConnectionError as errc:
            log.error(f"Error Connecting: {errc}")

        except requests.exceptions.Timeout as errt:
            log.error(f"Timeout Error: {errt}")

        except requests.exceptions.RequestException as err:
            log.error(f"Error: {err}")

        finally:
            return response

    class _DataAccess:
        def __init__(self, parent):
            self.parent = parent

        def dataquery(self, mode, **kwargs):
            command = "dataquery"
            valid_modes = [
                "most-recent",
                "since-time",
                "since-record",
                "date-range",
                "backfill",
            ]
            assert mode in valid_modes, f"mode must be one of {valid_modes}"

            valid_kwargs = [
                "format",
                "records",
                "time",
                "record",
                "start",
                "end",
                "interval",
                "table",
                "field",
            ]
            for key in kwargs:
                assert key in valid_kwargs, f"invalid keyword argument: {key}"

            valid_formats = ["html", "json", "toa5", "tob1", "xml"]
            if "format" in kwargs:
                assert (
                    kwargs["format"] in valid_formats
                ), f"format must be one of {valid_formats}"

            def _get_data(**kwargs):
                data = {}
                if "table" in kwargs:
                    table = kwargs["table"]
                    kwargs.pop("table")
                    data[table] = self.parent._api_request(
                        command, table=table, **kwargs
                    )
                else:
                    for table in self.parent.tables:
                        data[table] = self.parent._api_request(
                            command, table=table, **kwargs)

                return data

            if mode == "most-recent":
                assert "records" in kwargs, "records (int) must be provided"
                assert isinstance(kwargs["records"],
                                  int), "records must be an int"

                parameter = kwargs["records"]

                return _get_data(
                    mode=mode, parameter1=parameter, **kwargs
                )

            elif mode == "since-time":
                assert "time" in kwargs, (
                    "time (datetime.datetime) must be provided"
                )
                assert isinstance(
                    kwargs["time"], datetime.datetime
                ), "time must be a datetime.datetime object"

                parameter = kwargs["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")

                return _get_data(
                    mode=mode, parameter1=parameter, **kwargs
                )

            elif mode == "since-record":
                assert "record" in kwargs, "record (int) must be provided"
                assert isinstance(kwargs["record"],
                                  int), "record must be an int"

                parameter = kwargs["record"]

                return _get_data(
                    mode=mode, parameter1=parameter, **kwargs
                )

            elif mode == "date-range":
                assert "start" in kwargs and "end" in kwargs, "".join(
                    [
                        "start (datetime.datetime) ",
                        "and end (datetime.datetime) must be provided",
                    ]
                )
                assert isinstance(kwargs["start"], datetime.datetime) and \
                    isinstance(kwargs["end"], datetime.datetime), \
                    "start and end must be datetime.datetime objects"

                parameter1 = kwargs["start"].strftime("%Y-%m-%dT%H:%M:%S.%f")
                parameter2 = kwargs["end"].strftime("%Y-%m-%dT%H:%M:%S.%f")

                return _get_data(
                    mode=mode,
                    parameter1=parameter1,
                    parameter2=parameter2,
                    **kwargs,
                )

            elif mode == "backfill":
                assert (
                    "interval" in kwargs
                ), "interval (datetime.timedelta) must be provided"
                assert isinstance(
                    kwargs["interval"], datetime.timedelta
                ), "interval must be a datetime.timedelta object"

                parameter = int(kwargs["interval"].total_seconds())

                return _get_data(
                    mode=mode, parameter1=parameter, **kwargs
                )

        query = dataquery  # alias

        def browsesymbols(self, **kwargs):
            valid_kwargs = ["table", "format"]
            for key in kwargs:
                assert key in valid_kwargs, f"invalid keyword argument: {key}"

            valid_formats = ["html", "json", "xml"]
            if "format" in kwargs:
                assert (
                    kwargs["format"] in valid_formats
                ), f"format must be one of {valid_formats}"

            command = "browsesymbols"
            format = kwargs.get("format", "json")

            return self.parent._api_request(command, format=format, **kwargs)

        symbols = browsesymbols  # alias

    class _ControlCommand:
        def __init__(self, parent):
            self.parent = parent

        def setvaluex(self, table, field, value, **kwargs):
            import warnings

            warnings.warn("This function is untested")

            return self.parent._api_request("setvaluex",
                                            table=table,
                                            field=field,
                                            value=value,
                                            **kwargs)

        def clockcheck(self, **kwargs) -> Union[dict, str]:
            """
            Returns the current time of the data logger
            """
            command = "ClockCheck"
            return self.parent._api_request(command, **kwargs)

        def clockset(self,
                     time: datetime.datetime,
                     **kwargs) -> Union[dict, str, None]:
            import warnings

            warnings.warn("This function is untested")
            return self.parent._api_request("ClockSet",
                                            time=time.strftime(
                                                "%Y-%m-%dT%H:%M:%S.%f"))

    class _FileManagement:
        def __init__(self, parent):
            self.parent = parent

        def newestfile(self):
            raise NotImplementedError("This function is not yet implemented")

        def listfiles(self):
            raise NotImplementedError("This function is not yet implemented")

        def filecontrol(self):
            raise NotImplementedError("This function is not yet implemented")

        def addfile(self, filename: str) -> requests.Response:
            import warnings

            warnings.warn("This function is untested")

            username = self.parent.username
            password = self.parent.password
            auth = f"{username}:{password}".encode("utf-8")
            authentication = base64.b64encode(auth)
            authentication = str(authentication, encoding="utf-8")
            headers = {"Authorization": f"{authentication}"}
            url = f"http://{self.parent.address}/CPU/{filename}"

            with open(filename, "rb") as payload:
                result = requests.put(url, headers=headers, data=payload)

            return result
