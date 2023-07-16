import falcon
from .submit import Submit
import queue

app = application = falcon.App()

submit = Submit()
app.add_route('/submit', submit)