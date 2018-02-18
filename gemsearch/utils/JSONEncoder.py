import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    """ Custom json encoder to serialize MongoDB object ids.
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
        