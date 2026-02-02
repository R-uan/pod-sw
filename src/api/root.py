import functions_framework
import flask


@functions_framework.http
def star_wars_api(request: flask.Request):
  print(request.method)
