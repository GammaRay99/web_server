import socket
import utils



class WebApp(object):
	def __init__(self, port=8080):
		self.port = port
		self.ip = "0.0.0.0"

		self.paths = {
				'GET': { '/favicon.ico': lambda: self.file("ico.png"),
						 '/404': utils.sample_404 },

				'POST': { '/404': utils.sample_404 }
				}

		self.server = None

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
		self.server = socket.socket()
		self.server.bind((self.ip, self.port))
		self.server.listen()

	def run(self, keep_log=True) -> None:
		"""
		Main loop of the web server
		:param keep_log: Determine either or not the server should keep
		track of the connexions. They are stored in a txt file named "log.txt"
		"""
		if keep_log:
			with open("log.txt", 'w') as f:
				pass

		while True:
			client, _ = self.server.accept()
			request = self._get_request(client)


			if keep_log:
				utils.log(f"{request.headers['Host']} - {request.action} {request.path}")

			# If the path exists, we send the corresponding file
			# If not, we send the 404 page
			try:
				headers = utils.HTTP_RESPONSE_HEADERS(200)
				content = self.paths[request.action][request.path]()
			except KeyError:
				headers = utils.HTTP_RESPONSE_HEADERS(404)
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

	def file(self, pathname: str) -> bytes:
		"""
		Returns any file as bytes
		:param pathname: the name of the file
		:return: file as bytes
		:rtype: bytes
		"""
		with open(pathname, "rb") as img:
			return img.read()
