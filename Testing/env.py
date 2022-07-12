#from dotenv import load_dotenv
#load_dotenv()

import os
user_name= os.environ.get("username")
password = os.environ.get("password")

print(user_name,password)
