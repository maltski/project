Hello!

To run this application, you only need to have made the installations specified here: https://cybersecuritybase.mooc.fi/installation-guide.

To run the server:
1. git clone https://github.com/maltski/project.git
2. Run (on windows):
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
3. Open your localhost as specified in the command prompt after starting the server.

Now that, this is complete, let us move into the essay, where flaws and fixes are described.


For this project, I have built a flawed application using Python and Django templates. In my flawed application, there are several security risks. We will focus on four of the “Top 10 Web Application Security Risks” provided by OWASP in 2017 [1], as well as Cross-Site Request Forgery (CSRF).


1.	Sensitive data exposure (A3)
-	“Sensitive data exposure refers to the accidental or deliberate disclosure of critical information” [2]. Data loss and disruption are common symptoms of injection attacks.
-	The addquestion form uses GET to submit the form fields, meaning that the form data, including the password, which is asked for, is included in the URL. This means that sensitive information in user input, will be visible in the browser's address bar, potentially leading to unintended exposure.
-	The form redirects you to a dedicated ‘addquestion’ page. Every form data will be visible in the URL until making the next action. After adding all the questions you want, you can return to the home page by clicking ‘Return home’. The questions will be displayed here.
-	To avoid including the form inputs in the URL, change the form method to POST in both index.html and addquestion.html. Also change GET to POST in the addquestion function in views.py.

Note:
-	The password itself is not needed to add a question as it is not validated, but the field does maliciously intend to lure users into submitting their passwords in plain text format.
-	Another way of avoiding the issue with the password being exposed is to delete the entire field, as no other function depends on the data retrieved through it.

Fixes:

GET->POST: https://github.com/maltski/project/blob/main/polls/forms.py#L8
https://github.com/maltski/project/blob/main/polls/templates/polls/addquestion.html#L4
https://github.com/maltski/project/blob/main/polls/views.py#L97
https://github.com/maltski/project/blob/main/polls/views.py#L105
Remove password from AddQuestion class: https://github.com/maltski/project/blob/main/polls/views.py#L59
Remove password from html: https://github.com/maltski/project/blob/main/polls/templates/polls/addquestion.html#L4
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L34

2.	Insufficient logging and monitoring (A10)
-	In the current application there is no log for debugging.
-	“Attackers rely on the lack of monitoring and timely response to achieve their goals without being detected” [3]. That is why the fixed code includes a logger for failed login attempts to detect, for example, attempted brute force attacks. If an attacker tries to login several times, the log will be full of notes about failed attempts, which will alert the responsible person for the page about a potential issue.
-	We create a log in settings.py and add a couple of logging statements in the login function in views.py.

Fixes:

Create logger: https://github.com/maltski/project/blob/main/project/settings.py#L127

Add logging statements: https://github.com/maltski/project/blob/main/polls/views.py#L45


3.	CSRF-protection
-	An attacker commits cross-site request forgery when he or she tricks the the victim into submitting a malicious request. CSRF is usually combined with social engineering in the form of e-mails or other messages including links that make the users forcefully make transactions to the attacker, for instance. “If the victim is an administrative account, CSRF can compromise the entire web application.” [4]
-	In this application, there is no CSRF-protection. None of the forms in the templates use CSRF-tokens and I have commented out the line “'django.middleware.csrf.CsrfViewMiddleware',” in settings.py.
-	To fix this, uncomment {% csrf_token %} in all the forms and also uncomment the line mentioned above to fix the imminent issue.
-	All POST forms that are targeted at internal URLs should use the {% csrf_token %} template tag.
Fixes:

Settings: https://github.com/maltski/project/blob/main/project/settings.py#L48

CSRF tokens: https://github.com/maltski/project/blob/main/polls/templates/polls/detail.html#L7
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L27
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L44
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L50
https://github.com/maltski/project/blob/main/polls/templates/polls/login.html#L4
https://github.com/maltski/project/blob/main/polls/templates/polls/addquestion.html#L5
https://github.com/maltski/project/blob/main/polls/templates/polls/addquestion.html#L17
https://github.com/maltski/project/blob/main/polls/templates/polls/register.html#L11

4.	Security misconfiguration (A6)
-	DEBUG is currently set to True in settings.py. This makes it possible to study the configuration of the page as an unauthorised user. This can be done simply by changing the URL to an invalid one in the search bar or by pressing the mystery button at the bottom of the index page. When pressing the mystery button, you will see an actual debugging of a made-up exception.
-	To protect the site from this, set DEBUG to False and ALLOWED_HOSTS to your localhost (usually ’27.0.0.1’) in settings.py and the mystery button will redirect to a 500 page instead.
-	“Debugging mode provides detailed error messages and other sensitive information that can be useful for attackers to gain insight into the inner workings of an application.” [5]

Fixes:

Debug to False: https://github.com/maltski/project/blob/main/project/settings.py#L27

Allowed_hosts: https://github.com/maltski/project/blob/main/project/settings.py#L29

5.	Cross-site scripting (XSS) (A7)
-	Cross-site scripting is a type of attack where an attacker can send malicious code, typically a browser side script, to another user through a web application. Flaws that make XSS possible occur when an application uses user input in its output without sanitising it. [6]
-	The inputs in the forms of this application are not properly sanitised before rendering. This makes it possible for hackers to include malicious scripts in their inputs to the site, for example, through the addquestion form. The form fields could look like this:

o	Question: <script>alert('XSS attack');</script>
o	Choice 1: <img src="invalid-image" onerror="alert('XSS attack');">
o	Choice 2: whatever
o	Password: malicious password

-	When the fields would be rendered into the page, the script tags would be included in the HTML.

-	We can stop this by using Django’s template engine to automatically escape user inputs. In the html files there are several {% autoescape off %} tags. Changing ‘off’ to ‘on’ will reactivate Djangos autoescape and sanitise the user input.

-	For the addquestion form, follow the instructions for sensitive data exposure as well as injection. The code that fixes those issues already includes measures for escaping untrusted input. While ‘form.cleaned_data’ uses autoescape, an additional layer of security is added with the escape function wrapped around it.

Fixes:

Uncommenting autoescape off: https://github.com/maltski/project/blob/main/polls/templates/polls/detail.html#L1
https://github.com/maltski/project/blob/main/polls/templates/polls/index.html#L11
https://github.com/maltski/project/blob/main/polls/templates/polls/results.html#L1 
https://github.com/maltski/project/blob/main/polls/templates/polls/addquestion.html#L3
https://github.com/maltski/project/blob/main/polls/templates/polls/login.html#L2
https://github.com/maltski/project/blob/main/polls/templates/polls/register.html#L9

In summary, sensitive data exposure, insufficient logging, CSRF, security misconfiguration (DEBUG mode) and XSS are the five weaknesses of the code that have been fixed. The application contains a fair few more, including broken authentication and broken access control. However, one must start somewhere and applying the fixes suggested in this essay takes this application five steps closer to cyber security. 

Merry Christmas and a happy new year!

References:
[1] https://owasp.org/www-project-top-ten/2017/
[2] https://www.manageengine.com/data-security/what-is/sensitive-data-exposure.html
[3] OWASP Top Ten 2017 | A10:2017-Insufficient Logging & Monitoring | OWASP Foundation
[4] https://owasp.org/www-community/attacks/csrf
[5] https://medium.com/@cfqbcgwkg/why-using-debug-true-in-a-production-environment-is-a-security-risk-709af72b3580
[6] https://owasp.org/www-community/attacks/xss/




