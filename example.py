import webserver


app = webserver.WebApp(port=666)
app.init()

@app.load_path("/home")
def home():
	count = int(app.read_file('./dynamic/count.wb')) + 1
	with open('./dynamic/count.wb', "w") as file:
		file.write(str(count))

	app.response_type = "text/html"
	return f"<h1>{str(count)} post requests</h1>"

@app.load_path("/home", method="POST")
def home():
	app.response_type = "json"
	count = int(app.read_file('./dynamic/count.wb')) + 1
	with open('./dynamic/count.wb', "w") as file:
		file.write(str(count))

	return "{'current count': " + str(count) + "}"


app.run(keep_log=True)
