# NOTE: WHEN YOU CREATE A NEW SQLALCHEMY MODEL, YOU MUST DO THE FOLLOWING:
# 1. Ensure "db" is being imported into the models file from "project.extensions"
# 2. The model must be imported into this file (see below)
# 3. Go to project __init__.py file and import model. It won't be explicitly used, but
#     it must be there for context.


from project.models.user import User
from project.models.blogpost import BlogPost
from project.models.user_profile_settings import UserProfileSettings
