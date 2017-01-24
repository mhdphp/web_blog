import uuid

import datetime
from flask import session

from src.common.database import Database
from src.models.blog import Blog


class User(object):

    # the main variable in user model
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    # use @classmethod for having returned an user object
    @classmethod
    def get_by_email(cls, email):
        # check the database, users collection for the pair email, password
        data = Database.find_one(collection='users', query={'email': email})
        if data is not None:
            # return the object user
            return cls(**data)

    # the same with this one
    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one(collection='users', query={'_id': _id})
        if data is not None:
            # return the object user
            return cls(**data)

    # not use self
    @staticmethod
    def login_valid(email, password):
        # User.login_valid('mihai@email.com', '1234')
        # check whether a user's email matched the password provided
        user = User.get_by_email(email)
        if user is not None:
            # check the password
            return user.password == password
        return False

    # @staticmethod
    # def register(email, password):
    #     user = User.get_by_email(email)
    #     if user is None:
    #         # user doesn't exist, so we can create is
    #         new_user = User(email, password)
    #         new_user.save_to_mongo()
    #         return True
    #     else:
    #         # if user exists
    #         return False


    # the second alternative is with @classmethod
    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, password)
            new_user.save_to_mongo()
            # put the email of the user in a session variable
            # from flask import session
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        # login_valid has already been called
        session['email'] = user_email


    @staticmethod
    def logout():
        session['email'] = None


    def get_blogs(self):
       # get all the blogs that have author_id
       return Blog.find_by_author_id(self._id)


    # create new blog with user_id = author_id
    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author=self.email,
                    title=title,
                    description=description,
                    author_id=self._id)

        blog.save_to_mongo()


    # create new post
    @staticmethod
    def new_post(blog_id, title, content, date=datetime.datetime.utcnow()):
        # title, content, date=datetime.datetime.utcnow()
        # find the blog in which the new post will be saved
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title=title,
                      content=content,
                      created_date=date)

    def json(self):
        return {
            "email":    self.email,
            "_id":      self._id,
            "password": self.password
        }


    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())