Hello!

To run this application, you only need to have made the installations specified here: https://cybersecuritybase.mooc.fi/installation-guide.

To run the server:
1. Download the application
2. Open command prompt
3. Run (on windows):
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
4. Open your localhost as specified in the command prompt after starting the server.

Now that, this is complete, let us move into the essay, where flaws and fixes are described.


For this project, I have built a flawed application using Python and Django templates. In my flawed application, there are several security risks. We will focus on four of the “Top 10 Web Application Security Risks” provided by OWASP [1], as well as Cross-Site Request Forgery (CSRF).


1.	Sensitive data exposure (A3)
-	“Sensitive data exposure refers to the accidental or deliberate disclosure of critical information” [2]. Data loss and disruption are common symptoms of injection attacks.
-	The addquestion form uses GET to submit the form fields, meaning that the form data, including the password, which is asked for, is included in the URL. This means that sensitive information in user input, will be visible in the browser's address bar, potentially leading to unintended exposure.
-	The form also does not work properly, as there are, at first, no questions displayed when using GET in this case. However, when you go back to the polls/ page and refresh it, the question(s) will appear in the list.
-	To avoid including the form inputs being included in the URL, change the form method to POST. But now, the page does not work. Let us look at the next flaw to fix the entire problem.

Note:
-	The password itself is not needed to add a question as it is not validated, but the field does maliciously intend to lure users into submitting their passwords in plain text format.
-	Another way of avoiding the issue with the password being exposed is to delete the entire field, as no other function depends on the data retrieved through it.

Fixes:

GET->POST: https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L25

2.	Injection (A1)
-	“SQL injection (SQLi) attacks involve inserting malicious code into a SQL query through user input, which is then executed by a website’s backend database server” [3]. 
-	There is a risk for injection with the form fields, as the questions and choices are stored in an SQLite database. This is mainly due to the complete lack of data validation.
-	The fix to this can be found commented out in the file ‘views.py’. To try it out, replace the current addquestion function in the same file with the new addquestion function. Comment out the last row of the class ‘AddQuestion’.
-	We also need to make changes in index.html. We must uncomment the form.as_p tag and comment out all the normal html input fields except the submit field.
-	Now the page works again after the changes regarding the previous flaw, and it is safer to use.
  
Fixes:

Current addquestion: https://github.com/maltski/project/blob/main/polls/views.py#L61
AddQuestion class row to remove: https://github.com/maltski/project/blob/main/polls/views.py#L59
New addquestion: https://github.com/maltski/project/blob/main/polls/views.py#L77
Uncomment form.as_p: https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L27
Comment html input fields: https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L28

3.	CSRF-protection
-	An attacker commits cross-site request forgery when he or she tricks the the victim into submitting a malicious request. CSRF is usually combined with social engineering in the form of e-mails or other messages including links that make the users forcefully make transactions to the attacker, for instance. “If the victim is an administrative account, CSRF can compromise the entire web application.” [4]
-	In this application, there is no CSRF-protection. None of the forms in the templates use CSRF-tokens and I have commented out the line “'django.middleware.csrf.CsrfViewMiddleware',” in settings.py.
-	To fix this, uncomment {% csrf_token %} in all the forms and also uncomment the line mentioned above to fix the imminent issue.
-	All POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag.
  
Fixes:

Settings: https://github.com/maltski/project/blob/main/project/settings.py#L47
CSRF tokens: https://github.com/maltski/project/blob/main/polls/templates/polls/detail.html#L6
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L26
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L42
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L47
https://github.com/maltski/project/blob/main/polls/templates/polls/login.html#L3

4.	Security misconfiguration (A6)
-	DEBUG is currently set to True in settings.py. This makes it possible to study the configuration of the page as an unauthorised user. This can be done simply by changing the URL to an invalid one in the search bar or by pressing the mystery button at the bottom of the index page. When pressing the mystery button, you will see an actual debugging of a made-up exception.
-	To protect the site from this, set DEBUG to False and ALLOWED_HOSTS to your localhost (usually ’27.0.0.1’) in settings.py and the mystery button will redirect to a 500 page instead.
-	“Debugging mode provides detailed error messages and other sensitive information that can be useful for attackers to gain insight into the inner workings of an application.” [5]

Fixes:

Debug to False: https://github.com/maltski/project/blob/main/project/settings.py#L26
Allowed_hosts: https://github.com/maltski/project/blob/main/project/settings.py#L28

5.	Cross-site scripting (XSS) (A7)
-	Cross-site scripting is a type of attack where an attacker can send malicious code, typically a browser side script, to another user through a web application. Flaws that make XSS possible occur when an application uses user input in its output without sanitising it. [6]
-	The inputs in the forms of this application are not properly sanitised before rendering. This makes it possible for hackers to include malicious scripts in their inputs to the site, for example, through the addquestion form. The form fields could look like this:

o	Question: <script>alert('XSS attack');</script>
o	Choice 1: <img src="invalid-image" onerror="alert('XSS attack');">
o	Choice 2: whatever
o	Password: malicious password

-	When the fields would be rendered into the page, the script tags would be included in the HTML.

-	We can stop this by using Django’s template engine to automatically escape user inputs. In the html files there are several commented autoescape tags. Uncommenting them will sanitise the user input.

-	For the addquestion form, follow the instructions for sensitive data exposure as well as injection. Included in the code fixing those issues is already, measures for escaping untrusted input. While ‘form.cleaned_data’ uses autoescape, an additional layer of security is added with the escape function wrapped around it.

Fixes:

Uncommenting autoescape: https://github.com/maltski/project/blob/main/polls/templates/polls/detail.html#L10
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L15
https://github.com/maltski/project/blob/main/polls/templates/polls/results.html#L5
https://github.com/maltski/project/blob/main/polls/templates/polls/results.html#L6
https://github.com/maltski/project/blob/main/polls/templates/polls/results.html#L7

In summary, sensitive data exposure, injection, CSRF, security misconfiguration (DEBUG mode) and XSS are the five weaknesses of the code that have been fixed. The application contains a fair few more, including broken access control and broken authentication. However, one must start somewhere and applying the fixes suggested in this essay takes this application five steps closer to cyber security. 

Merry Christmas and a happy new year!

References:
[1] https://owasp.org/www-project-top-ten/2017/
[2] https://www.manageengine.com/data-security/what-is/sensitive-data-exposure.html
[3] https://www.zscaler.com/blogs/product-insights/owasp-top-10-injection-attacks-explained
[4] https://owasp.org/www-community/attacks/csrf
[5] https://medium.com/@cfqbcgwkg/why-using-debug-true-in-a-production-environment-is-a-security-risk-709af72b3580
[6] https://owasp.org/www-community/attacks/xss/

