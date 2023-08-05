import falcon
from .submit import Submit
from dotenv import load_dotenv
load_dotenv()

app = application = falcon.App(cors_enable=True)

submit = Submit()
app.add_route('/submit', submit)