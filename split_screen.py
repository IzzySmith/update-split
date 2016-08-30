from __future__ import print_function 
import re
import json
import sys
import mandrill
from flask import Flask, request, make_response, render_template
from werkzeug.routing import Rule, Map, BaseConverter, ValidationError


app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

surfly_encoded_logo = 'iVBORw0KGgoAAAANSUhEUgAAAFYAAAAkCAMAAAAkYj0PAAAANlBMVEXlR0b////lR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0blR0beFbDIAAAAEXRSTlMAABAgMEBQYHCAj5+vv8/f7/4ucL8AAALfSURBVHjatZbZttsgDEV9AYGxmfz/P1uhATwkadrV8hAbkLeEjoAsPz8/y181u+YDW03hNkHIiTVkV6L5ihqJ2fpvMR+wrh7cmvuWWhZHj/Aea8lxtAtsX3CBArD4Ar37HpuJynGnT8Rp3c0gplwO9w5ryL24Xu0H4rRelX+8jRbOWIPPvr7AwYMnNxb7BiKgQJ6tcZhSl9VuYTuAK3YTf26pYr5qNKX3QyNJk6gbFqufJbFz7PCahJEkczEvMoBQ6m70qKivF/wtDDMk2y/FBRfzpAPNEnFpqljkYG5h1HOBDe7DPOpA4Kfl0aGYel016tN28HMzjFRNJXea44nkZXQqFnlEwzhv3nCIECLQUdTc4AB/b8ixjk7F9ksYnrFPLj13TRXOybJ9LbtbsoyqYvcwLGMfXNsuqZoSUnsodgujyXZ4cl2jVIFqs553iyg2JRDsJjP5hDWAzSBucqMtnKqROxFXRjXjHcvcyg4VC3uVSvdFuByoHFQzm7P67AhyhK1rZazLvGsytgZiAZqQmbusx5cU20zpIqus7JCwgQb01HK63yw9ac46XtxZsUxv4yQzIcbogBXrWC9fzLZyPkw99sJv4VwIdvqIp405+omwVW1mS5Je3Lxr6ldg2OKKgsp69hgBeHE+5WhvH64dC93f9Y7TOjHfXJaaOronK0mh2Hy3qoxtu/0KanJc+v1ruF461nUtn1cVjcaGJ/fvqb5hFrsEjutNc1teRgsYBoLb9vkitpnEGdJaxgIRnrlNvL5QqfreQnepC/4k9Gr70bqtV3H2y1+V0MOpG7zIaZ9SLOfNzZs34Er9cj1w0tmR2+lqTBFG1P0O7syJFe7E0krK6tjc9w484ioCKJma9CZWtr+fWPqsb6hG5uW1RnYtZ9ATm7T+J3b8bxjLfE1Ob7EtYP3EC/ZPGqz45+PekInhBAz3b7CTDTFulGM8HwKovPUq2b9qcGz/A4uZEOwvoTZPQ1Kv5d4AAAAASUVORK5CYII='

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/splitscreen')
def splitscreen():
   return render_template('splitscreen.html')

@app.route('/<regex("[0-9]{3}[-][0-9]{3}[-][0-9]{3}"):session_id>/')
def index_session_id(session_id):
   return render_template('follower_side.html')

@app.route('/share', methods = ['POST', 'GET'])
def share():
   if request.method == 'POST':
      try:
         email_address = request.form[ 'emailAddress' ]
         email_link = request.form[ 'inviteLink' ]
         mandrill_client = mandrill.Mandrill('your_key_here')
         message = {
            'from_email': 'splitscreen@surfly.com',
            'to': [{'email': email_address}],
            'html':'<h4>You have been invited to a splitscreen session!</h4><p><a   href='+email_link+'>Join the session</a></p><p><img src="cid:logo"/></p>',
            'subject':'Invitation to a splitscreen session',
            'images': [{'content': surfly_encoded_logo,
                    'name': 'logo',
                    'type': 'image/png'}]}
         result = mandrill_client.messages.send(message=message, async=False) 
         return render_template('fourth_frame.html')
      except mandrill.Error, e:
         return render_template('error.html', error=e)
         raise
   else:
      return render_template('share.html')

