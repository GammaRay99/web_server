import webserver


app = webserver.WebApp(port=666)
app.init()


@app.load_path("/home")
def home():
	return """<h1>Hello World</h1>"""


app.run(keep_log=True)
