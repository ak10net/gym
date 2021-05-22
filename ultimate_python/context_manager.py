""" 
Context managers are used to open and close resources as python
enters and exits a code block respectively. Some examples of the resource
it can manage are files, database connections and sockets.
In this module, we simulate how a context manager can handle open and close
operations of a file-like object called StringIO.
"""

from contextlib import contextmanager
from io import StringIO

# Simple directory with file contents
_FILESYSTEM = {
	"a.txt": "Hello World",
	"b.xml": "<message>Hello World</message>",
	"c.out": "10101010"
}

# Function based context manager
@contextmanager
def file(filename):
	"""File contect manager"""
	io_buffer = StringIO(_FILESYSTEM[filename])
	try:
		# pass the buffer to context block
		yield io_buffer
	finally:
		# close the buffer unconditionally
		io_buffer.close()

# Class based context manager
class FileHandler:
	"""File handler context manager"""
	def __init__(self,filename):
		self.io_buffer = StringIO(_FILESYSTEM[filename])

	def __enter__(self):
		"""Pass the buffer"""
		return self.io_buffer

	def __exit__(self, *args):
		"""Close the buffer unconditionally"""
		self.io_buffer.close()


def main():
	# An exmaple of a function based context manager
	with file("a.txt") as txt_buffer:
		assert txt_buffer.read() == "Hello World"

	# An example of class based context manager
	with FileHandler("b.xml") as xml_buffer:
		assert xml_buffer.read() == "<message>Hello World</message>"

	for context_obj in (file, FileHandler):
		call_failed = False
		try:
			with context_obj("c.out"):
				raise RuntimeError("System crash. Abort!")
		except RuntimeError:
			call_failed = True
		assert call_failed is True


if __name__ == "__main__":
	main()