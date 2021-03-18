import socket



def HTTP_RESPONSE_HEADERS(status_code: int) -> str:
	"""
	Returns a HTTP response with corrects header

	:param status_code: The status code of the HTTP request
	:return: Valid HTTP header response
	:rtype: str
	"""
	head = f"HTTP/1.1 {status_code} OK\n"
	next_lines = """Date: Fri, 16 Jun 2021 23:59:59 UTC
NotAHeader: what
Content-Type: text/html

"""
	return (head + next_lines).encode("utf-8")



class Request(object):
	"""
	A Request object have 5 attributes:
		-raw_content: The list of all the headers 
		-action: The action submitted (should be either "GET" or "POST")
		-path: The path requested
		-protocol: The protocol and the version of transmission
		-headers: A dict listing all the headers
	"""
	def __init__(self, raw_request: str):
		self.raw_content = [line[:-1] for line in raw_request.split('\n')]

		start = self.raw_content[0].split(' ')
		self.action = start[0]
		self.path = start[1]
		self.protocol = start[2]

		self.headers = {}
		# TODO: are the 2 last lines of a http request always empty ?
		for line in self.raw_content[1:]:
			if not line:
				continue

			header = line.split(':')
			self.headers[header[0]] = ':'.join(header[1:])


class MethodError(Exception):
	def __init__(self, content=None):
		self.content = content

	def __str__(self):
		return self.content if self.content is not None else "Method not allowed, only GET and POST sould be used."

class PathNameError(Exception):
	def __init__(self, content=None):
		self.content = content

	def __str__(self):
		return self.content if self.content is not None else "Path name should always starts with \"/\""


def log(content: str):
	with open("log.txt", "a") as f:
		f.write('\n')
		f.write(content)


def sample_404():
	return """<html>
<body>
<h1>Error 404, page not found.</h1>
</body>
</html>"""


def sample_ico():
	with open("ico.png", "rb") as img:
		return img.read()
