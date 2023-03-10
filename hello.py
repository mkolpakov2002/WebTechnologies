def app(environ, start_response):
	querystring = environ['QUERY_STRING']
	lines = querystring.split("&")
	result = ""
	for l in lines:
		result += l.strip() + "\r\n"

	start_response("200 OK", [
		("Content-Type", "text/plain"),
		("Content-Length", str(len(result)))
	])

	return result