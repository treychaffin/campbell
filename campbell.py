import requests
import datetime
import base64
from typing import Union

import logging

logging.basicConfig(level=logging.DEBUG)


class Campbell:
    """
    Used to interface with Campbell Scientific data loggers via the web API

    https://help.campbellsci.com/crbasic/cr1000x/Content/Info/webserverapicommands1.htm
    """

    def __init__(
        self,
        address: str,
        tables: list,
        **kwargs,
    ) -> None:
        """
        Initializes the class with the address of the data logger
        and a list of tables
        """
        self.address: str = address
        self.tables: list = tables
        self.timeout = kwargs.get("timeout", 10)
        if "username" in kwargs and "password" in kwargs:
            self.username = kwargs["username"]
            self.password = kwargs["password"]

        self.DataAccess = self._DataAccess(self)
        self.ControlCommand = self._ControlCommand(self)
        self.FileManagement = self._FileManagement(self)

    # def _api_request(self, command: str, **kwargs) -> Union[dict, str]:
    def _api_request(self, command: str, **kwargs) -> None:

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

        if "value" in kwargs:
            url += f"&value={kwargs['value']}"

        if "mode" in kwargs:
            url += f"&mode={kwargs['mode']}"

        if "format" in kwargs:
            url += f"&format={kwargs['format']}"

        if "time" in kwargs and command == "ClockSet":
            url += f"&time={kwargs['time']}"

        if "parameter1" in kwargs:
            url += f"&p1={kwargs['parameter1']}"

        if "parameter2" in kwargs:
            url += f"&p2={kwargs['parameter2']}"

        if "format" in kwargs and kwargs["format"] == "json":
            # return self._request(url).json()
            return self._request(url)
        else:
            # return self._request(url).text
            return self._request(url)

    # def _request(self, url) -> requests.Response:
    # try:
    #     response = requests.get(url, timeout=self.timeout)
    #     if response.status_code == 200:
    #         return response
    #     response.raise_for_status()

    # except requests.exceptions.HTTPError as errh:
    #     logging.error("Http Error:", errh)

    # except requests.exceptions.ConnectionError as errc:
    #     logging.error("Error Connecting:", errc)

    # except requests.exceptions.Timeout as errt:
    #     logging.error("Timeout Error:", errt)

    # except requests.exceptions.RequestException as err:
    #     logging.error("OOps: Something Else", err)

    # finally:
    #     return response

    def _request(self, url) -> None:
        print(url)

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
            ]
            for key in kwargs:
                assert key in valid_kwargs, f"invalid keyword argument: {key}"

            valid_formats = ["html", "json", "toa5", "tob1", "xml"]
            if "format" in kwargs:
                assert (
                    kwargs["format"] in valid_formats
                ), f"format must be one of {valid_formats}"

            format = kwargs.get("format", "json")  # default to json

            def _get_data(**kwargs):
                data = {}

                for table in self.parent.tables:
                    data[table] = self.parent._api_request(command, **kwargs)

                return data

            if mode == "most-recent":
                assert "records" in kwargs, "records (int) must be provided"
                assert isinstance(kwargs["records"], int), "records must be an int"

                parameter = kwargs["records"]

                return _get_data(
                    mode=mode, parameter1=parameter, format=format, **kwargs
                )

            elif mode == "since-time":
                assert "time" in kwargs, "time (datetime.datetime) must be provided"
                assert isinstance(
                    kwargs["time"], datetime.datetime
                ), "time must be a datetime.datetime object"

                parameter = kwargs["time"].strftime("%Y-%m-%dT%H:%M:%S.%f")

                return _get_data(
                    mode=mode, parameter1=parameter, format=format, **kwargs
                )

            elif mode == "since-record":
                assert "record" in kwargs, "record (int) must be provided"
                assert isinstance(kwargs["record"], int), "record must be an int"

                parameter = kwargs["record"]

                return _get_data(
                    mode=mode, parameter=parameter, format=format, **kwargs
                )

            elif mode == "date-range":
                assert "start" in kwargs and "end" in kwargs, "".join(
                    [
                        "start (datetime.datetime) ",
                        "and end (datetime.datetime) must be provided",
                    ]
                )
                assert isinstance(kwargs["start"], datetime.datetime) and isinstance(
                    kwargs["end"], datetime.datetime
                ), "start and end must be datetime.datetime objects"

                parameter1 = kwargs["start"].strftime("%Y-%m-%dT%H:%M:%S.%f")
                parameter2 = kwargs["end"].strftime("%Y-%m-%dT%H:%M:%S.%f")

                return _get_data(
                    mode=mode,
                    parameter1=parameter1,
                    parameter2=parameter2,
                    format=format,
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
                    mode=mode, parameter1=parameter, format=format, **kwargs
                )

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

    class _ControlCommand:
        def __init__(self, parent):
            self.parent = parent
            self.setvaluex_result_codes = {
                0: "An unrecognized failure occurred",
                1: "Success",
                2: "".join(
                    [
                        "The data source connection failed ",
                        "(LoggerNet data sources only)",
                    ]
                ),
                3: "LoggerNet logon failed (LoggerNet data sources only)",
                4: "Blocked by LoggerNet security (LoggerNet data sources only)",
                5: "Read only",
                6: "Invalid table name",
                7: "Invalid fieldname",
                8: "Invalid fieldname subscript",
                9: "Invalid field data type",
                10: "Datalogger communication failed",
                11: "Datalogger communication disabled (LoggerNet data sources only)",
                12: "Blocked by datalogger security",
                13: "Invalid table definitions (LoggerNet data sources only)",
                14: "Invalid device name (LoggerNet data sources only)",
                15: "Invalid web client authorization",
            }
            self.clock_result_codes = {
                1: "The clock was checked (successful)",
                2: "The clock was set",
                3: "The LoggerNet session failed (LoggerNet data sources only)",
                4: "Invalid LoggerNet logon (LoggerNet data sources only)",
                5: "Blocked by LoggerNet security (LoggerNet data sources only)",
                6: "Communication with the station failed (LoggerNet data sources only)",
                7: "Communication with the station disabled (LoggerNet data sources only)",
                8: "Blocked by datalogger security",
                9: "Invalid station name (LoggerNet data sources only)",
                10: "LoggerNet device is busy (LoggerNet data sources only)",
                11: "Specified URI does not reference a LoggerNet station (LoggerNet data sources only)",
            }

        def setvaluex(self, table, field, value, **kwargs):
            uri = f"dl:{table}:{field}"
            value = str(value)
            raise NotImplementedError("This function is not yet implemented")

        def clockcheck(self, **kwargs) -> Union[dict, str]:
            """
            Returns the current time of the data logger
            """
            command = "ClockCheck"
            return self.parent._api_request(command, **kwargs)

        def clockset(self, time: datetime.datetime):
            raise NotImplementedError("This function is not yet implemented")

    class _FileManagement:
        def __init__(self, parent):
            self.parent = parent

            # description of action commands, copied from API documentation
            self.action_descriptions = {
                1: "".join(
                    [
                        "Compile and run the file specified by File and mark ",
                        "it as the program to be run on power up.",
                    ]
                ),
                2: "".join(
                    [
                        "Mark the file specified by File as the program to ",
                        "be run on power up.",
                    ]
                ),
                3: "Mark the file specified by File as hidden.",
                4: "Delete the file specified by File.",
                5: "Format the device specified by File.",
                6: "".join(
                    [
                        "Compile and run the file specified by File without ",
                        "deleting existing data tables.",
                    ]
                ),
                7: "Stop the currently running program.",
                8: "".join(
                    [
                        "Stop the currently running program and delete ",
                        "associated data tables.",
                    ]
                ),
                9: "".join(
                    [
                        "Install the operating system (*.obj) specified by ",
                        "File. The file must reside on the datalogger's CPU ",
                        "drive (sent to the datalogger using HTTPPut)",
                    ]
                ),
                10: "".join(
                    [
                        "Compile and run the program specified by File but ",
                        "do not change the program currently marked to run ",
                        "on power up.",
                    ]
                ),
                11: "Pause execution of the currently running program.",
                12: "Resume execution of the currently paused program.",
                13: "".join(
                    [
                        "Stop the currently running program, delete its ",
                        "associated data tables, run the program specified ",
                        "by File, and mark the same file as the program to ",
                        "be run on power up.",
                    ]
                ),
                14: "".join(
                    [
                        "Stop the currently running program, delete its ",
                        "associated data tables, and run the program ",
                        "specified by File without affecting the program to ",
                        "be run on power up.",
                    ]
                ),
                15: "".join(
                    [
                        "Move the file specified by File2 to the name ",
                        "specified by File.",
                    ]
                ),
                16: "".join(
                    [
                        "Move the file specified by File2 to the name ",
                        "specified by File, stop the currently running ",
                        "program, delete its associated data tables, and run ",
                        "the program specified by File2 while marking it to ",
                        "run on power up.",
                    ]
                ),
                17: "".join(
                    [
                        "Move the file specified by File2 to the name ",
                        "specified by File, stop the currently running ",
                        "program, delete its associated data tables, and run ",
                        "the program specified by File2 without affecting ",
                        "the program that will run on power up.",
                    ]
                ),
                18: "".join(
                    [
                        "Copy the file specified by File2 to the name ",
                        "specified by File.",
                    ]
                ),
                19: "".join(
                    [
                        "Copy the file specified by File2 to the name ",
                        "specified by File, stop the currently running ",
                        "program, delete its associated data tables, and run ",
                        "the program specified by File2 while marking it to ",
                        "run on power up.",
                    ]
                ),
                20: "".join(
                    [
                        "Copy the file specified by File2 to the name ",
                        "specified by File, stop the currently running ",
                        "program, delete its associated data tables, and run ",
                        "the program specified by File2 without affecting ",
                        "the program that will run on power up.",
                    ]
                ),
            }

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
