from . import BaseClass
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WriteOptions, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WriteApi


class Client(BaseClass):
    """
    Influx db client used for writing data
    """
    _influx_client: InfluxDBClient = None
    token: str = os.environ.get("INFLUXDB_TOKEN")
    org: str
    url: str
    bucket: str
    write_options: WriteOptions = SYNCHRONOUS
    _write_api: WriteApi = None

    def write(self, record: Point) -> list:
        """
        Write a point to the DB
        :param record: influxdb_client.Point
        :return: list
        """
        if self._influx_client is None:
            self._influx_client = influxdb_client.InfluxDBClient(url=self.url, token=self.token, org=self.org)
        if self._write_api is None:
            self._write_api = self._influx_client.write_api(write_options=self.write_options)
        return self._write_api.write(bucket=self.bucket, org=self.org, record=record)


class LogLine(BaseClass):
    """
    This class should take a client, and matched line and trigger to write to influx
    """
    pass
