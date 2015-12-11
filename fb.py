import subprocess

import secrets

FB_NEW_LINE="%0A"

 
# name too long: pipe stuff to another .py or something.
 
message = "abc"
message += FB_NEW_LINE
message += "cde"

command =  """curl -i -X POST """
command += """ -d "message=%s" """ %message
command += """ -d "access_token=%s" """ %secrets.FB_ACCESS_TOKEN
command += """ https://graph.facebook.com/v2.5/me/feed/ """

print command

subprocess.call(command.split(" "))
