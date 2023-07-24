import falcon
from .submit import Submit
from dotenv import load_dotenv
load_dotenv()

app = application = falcon.App()

submit = Submit()
app.add_route('/submit', submit)