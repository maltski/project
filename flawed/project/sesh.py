import django.contrib.sessions.backends.db as db
from django.contrib.auth.models import User

class Session(db.SessionStore):
    counter = 0

    def get_key(self):
        key = User.objects.get(self)
        while self.exists(key):
            key = encrypt_text(key, Session.counter)
            Session.counter += range(len(key))

        return key
    
def encrypt_text(plaintext, n):
    ans = ""
    
    for i in range(len(plaintext)):
        ch = plaintext[i]
        
        if ch==" ":
            ans+=" "
        
        else:
            ans += chr(ord(ch) + n)
    
    return ans
