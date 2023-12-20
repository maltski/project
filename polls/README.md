Security risks:
1. CSRF
    - CSRF-token
    - exempt
    "Since we’re creating a POST form (which can have the effect of modifying data), we need to worry about Cross Site Request Forgeries. Thankfully, you don’t have to worry too hard, because Django comes with a helpful system for protecting against it. In short, all POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag."

2. sensitive data exposure
    - get instead of post

3. Check views.py def vote

4. Injection
    - Need some kind of sql and free text fields

5. Broken authentication
    - User can do other users tasks