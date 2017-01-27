import uuid
import datetime
from src.common.database import Database


class Post(object):
    # we can have default parameters in the end id=None
    def __init__(self, title, content, author, blog_id, created_date=datetime.datetime.utcnow(), _id=None):
        # id = post id, blog_id = blog id,
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self.blog_id = blog_id
        # generate a random id if we haven't got any id
        self._id = uuid.uuid4().hex if _id is None else _id

    #save data to mongo
    def save_to_mongo(self):
        Database.insert(collection = 'posts', data = self.json())

    # convert the data into json format
    def json(self):
        return {
            '_id':       self._id,
            'blog_id':  self.blog_id,
            'title':    self.title,
            'content':  self.content,
            'author':   self.author,
            'created_date': self.created_date
        }

    # @staticmethod
    # # return all posts with id = 'id' from collection = 'posts'
    # def from_mongo(id):
    #     return Database.find_one(collection='posts', query={'id':id})


    # we will use @classmethod instead of @staticmethod - the result will be an object
    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query={'_id':id})
        # return cls(title = post_data['title'],
        #            content = post_data['content'],
        #            author = post_data['author'],
        #            blog_id = post_data['blog_id'],
        #            created_date = post_data['created_date'],
        #            _id = post_data['_id'])

        # replace with the name of the field in post_data is the name of property of the object
        return cls(**post_data)


    @staticmethod
    # return all posts belonging to the blog with blog_id
    # return a list of them - list comprehension
    def from_blog(_id):
        return [post for post in Database.find(collection='posts', query={'blog_id':_id})]