from osdp import *
#from osdp._connection import SerialPortOsdpConnection

from abc import ABC, abstractmethod
import serial
import fcntl
import struct
import socket


class OsdpConnection(ABC):

	@property
	@abstractmethod
	def baud_rate(self) -> int:
		pass

	@property
	@abstractmethod
	def is_open(self) -> bool:
		pass

	@abstractmethod
	def open(self):
		pass

	@abstractmethod
	def close(self):
		pass

	@abstractmethod
	def write(self, buf: bytes):
		pass

	@abstractmethod
	def read(self, size: int = 1) -> bytes:
		pass


class SerialPortOsdpConnection(OsdpConnection):

	def __init__(self, port: str, baud_rate: int, raspberry_pi: bool = False):
		self._port = port
		self._baud_rate = baud_rate
		self.serial_port = None
		self.raspberry_pi = raspberry_pi

	@property
	def baud_rate(self) -> int:
		return self._baud_rate

	@property
	def is_open(self) -> bool:
		return self.serial_port is not None and self.serial_port.is_open

	def open(self):
		self.serial_port = serial.Serial(port=self._port, baudrate=self._baud_rate, timeout=2.0)
		if self.raspberry_pi:
			fd = self.serial_port.fileno()
			# See struct serial_rs485 in linux kernel.
			# SER_RS485_ENABLED = 1 and SER_RS485_RTS_ON_SEND = 1
			# https://www.kernel.org/doc/Documentation/serial/serial-rs485.txt
			serial_rs485 = struct.pack('IIIIIIII', 3, 0, 0, 0, 0, 0, 0, 0)
			fcntl.ioctl(fd, 0x542F, serial_rs485)

	def close(self):
		if self.serial_port is not None:
			self.serial_port.close()
			self.serial_port = None

	def write(self, buf: bytes):
		self.serial_port.write(buf)

	def read(self, size: int = 1) -> bytes:
		return self.serial_port.read(size)

if __name__ == '__main__':
    conn = SerialPortOsdpConnection(port='/dev/serial0', baud_rate=9600,raspberry_pi= True)
    cp = ControlPanel()
    bus_id = cp.start_connection(conn)
    cp.add_device(connection_id=bus_id, address=0x7F, use_crc=True, use_secure_channel=False)
    id_report = cp.id_report(connection_id=bus_id, address=0x7F)
    device_capabilities = cp.device_capabilities(connection_id=bus_id, address=0x7F)
    local_status = cp.local_status(connection_id=bus_id, address=0x7F)
    input_status = cp.input_status(connection_id=bus_id, address=0x7F)
    output_status = cp.output_status(connection_id=bus_id, address=0x7F)
    cp.shutdown()