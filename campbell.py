import requests
import datetime
from typing import Union

import logging

logging.basicConfig(level=logging.DEBUG)


class campbell:
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
        """Initializes the class with the address of the data logger and a list of tables"""
        self.address: str = address
        self.tables: list = tables
        self.time_offset: datetime.timedelta = kwargs.get(
            "time_offset", datetime.timedelta(hours=0)
        )

        # list acceptable formats as defined in API documentation
        self.formats: list = [
            "html",
            "json",
            "toa5",
            "tob1",
            "xml",
        ]

    def _data_access(
        self, command: str, table: str, format: str, mode: str, parameter: str
    ) -> requests.Response:
        """returns the response from the data logger"""
        url = f"http://{self.address}/?command={command}&uri=dl:{table}&format={format}&mode={mode}&{parameter}"
        response = requests.get(url)
        if response.status_code == 200:
            return response
        else:
            logging.error(
                f"Request failed with status code: {response.status_code} url: {url}"
            )
            response.raise_for_status()
            return response

    def _data(self, command: str, format: str, mode: str, parameter: str) -> dict:
        """returns the data from the response"""

        data: dict = {}

        for table in self.tables:
            if format == "json":
                data[table] = self._data_access(
                    command, table, format, mode, parameter
                ).json()
            else:
                data[table] = self._data_access(
                    command, table, format, mode, parameter
                ).text

        return data

    def _assert_format(self, format: str) -> None:
        assert format in self.formats, f"format must be one of {self.formats}"

    def most_recent(self, records: int = 1, **kwargs) -> dict:
        """
        Returns the data from the most recent number of records

        Parameters:
            records (int): the number of records to pull
        """

        command = "dataquery"
        format = kwargs.get("format", "json")
        self._assert_format(format)
        mode = "backfill"
        parameter = f"p1={records}"

        return self._data(command, format, mode, parameter)

    def since_time(self, time: datetime.timedelta, **kwargs) -> dict:
        """
        Returns all the data since a certain time

        Parameters:
            time (datetime.timedelta): the time to pull data since

        Returns:
            dict: a dictionary of the data since the time
        """

        now = datetime.datetime.now()
        since_time = now - time - self.time_offset

        command = "dataquery"
        format = kwargs.get("format", "json")
        self._assert_format(format)
        mode = "since-time"
        parameter = f"p1={since_time.strftime("%Y-%m-%dT%H:%M:%S.%f")}"

        return self._data(command, format, mode, parameter)

    def since_record(self, record: int, **kwargs) -> dict:
        """
        Returns all the data since a certain record

        Parameters:
            record (int): the record to pull data since

        Returns:
            dict: a dictionary of the data since the record
        """

        command = "dataquery"
        format = kwargs.get("format", "json")
        self._assert_format(format)
        mode = "since-record"
        parameter = f"p1={record}"

        return self._data(command, format, mode, parameter)

    def date_range(
        self, start: datetime.datetime, end: datetime.datetime, **kwargs
    ) -> dict:
        """
        Returns all the data between two dates

        Parameters:
            start (datetime.datetime): the start date
            end (datetime.datetime): the end date

        Returns:
            dict: a dictionary of the data between the two dates
        """

        command = "dataquery"
        format = kwargs.get("format", "json")
        self._assert_format(format)
        mode = "date-range"
        parameter = f"p1={start.strftime("%Y-%m-%dT%H:%M:%S.%f")}&p2={end.strftime("%Y-%m-%dT%H:%M:%S.%f")}"

        return self._data(command, format, mode, parameter)

    def backfill(self, interval: datetime.timedelta, **kwargs) -> dict:
        """
        Returns the data from the called interval

        Parameters:
            interval (datetime.timedelta): the interval to pull data from
        """

        command = "dataquery"
        format = kwargs.get("format", "json")
        self._assert_format(format)
        mode = "backfill"
        parameter = f"p1={int(interval.total_seconds())}"

        return self._data(command, format, mode, parameter)
