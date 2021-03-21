import socket
import os
import utils



class WebApp(object):
	def __init__(self, port=8080, ip="0.0.0.0"):
		self.port = port
		self.ip = ip

		self.paths = {
				'GET': { '/404': utils.sample_404 },
				'POST': { '/404': utils.sample_404 }
				}

		self.response_type = "text/html"

		self._server = None

	def _get_request(self, client: socket.socket) -> utils.Request:
		"""
		Waits for a connexion from a client and return a
		Request object.

		:param client: The client we are listening to
		:type client: socket.socket
		:return: A request object of the request the client sent
		:rtype: utils.Request
		"""
		request = client.recv(1024).decode("utf-8")

		return utils.Request(request)


	def init(self) -> None:
		"""
		Create a network endpoint binded at
		the IP and the PORT of the WebApp and
		open it for connexions.
		"""
		self._server = socket.socket()
		self._server.bind((self.ip, self.port))
		self._server.listen()

		path, static_files = utils.get_static_files()
		for filename in static_files:
			self.paths["GET"][filename] = self._send_file(path + filename)


	def run(self, keep_log=True) -> None:
		"""
		Main loop of the web server
		:param keep_log: Determine either or not the server should keep
		track of the connexions. They are stored in a txt file named "log.txt"
		"""
		print(f"Running web service on http://{self.ip}:{self.port}\nLOG = {keep_log}")
		if keep_log:
			with open("log.txt", 'w') as _:
				pass

		while True:
			client, _ = self._server.accept()
			request = self._get_request(client)
			if not request.http_request:
				continue


			if keep_log:
				utils.log(f"{request.headers['Host']} - {request.raw_content}")

			# If the path exists, we send the corresponding file
			# If not, we send the 404 page
			try:
				headers = utils.HTTP_RESPONSE_HEADERS(200, self.response_type)
				content = self.paths[request.action][request.path]()
			except KeyError:
				headers = utils.HTTP_RESPONSE_HEADERS(404, self.response_type)
				content = self.paths[request.action]['/404']()

			# Determines if we already converted the content to
			# bytes or not (png will already be bytes, text not)
			if type(content) == str:
				response = headers + content.encode("utf-8")
			else:
				response = headers + content

			# Send everthing
			client.send(response)
			client.close()

	def load_path(self, pathname: str, method="GET") -> None:
		"""
		Create a new key in our path dictionnary, and assign
		it the fuction passed as decorator's parameter.
		:param pathname: The relative name of the path "/some_name"
		:param method: The method for the path ("GET" or "POST" only)
		"""
		if pathname[0] != '/':
			raise utils.PathNameError()

		if method not in ("GET", "POST"):
			raise utils.MethodError()

		def wrapper(func) -> None:
			"""
			Adds the function to the dictionnary
			:param func: the function
			:type func: function
			"""
			self.paths[method][pathname] = func

		return wrapper


	def read_file(self, pathname:str) -> str:
		"""
		Simply reads a file and output the content

		:param pathname: path of the file
		:return: content of the file
		"""
		with open(pathname, "r") as f:
			return f.read()

	def _send_file(self, pathname: str): # -> function
		def wrapper():
			with open(pathname, "rb") as f:
				return f.read()
		return wrapper
