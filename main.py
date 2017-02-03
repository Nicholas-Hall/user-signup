#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2
import urllib
import re
USER_RE = re.compile (r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile (r"^.{3,20}$")
EMAIL_RE = re.compile (r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def pagebuild(username_input, password_input, verify_password_input, email_input, posted):
    header = "<h1>Sign in</h1>"

    test = valid_username(username_input)

    formpost = """ <form method="post" name="username"> """

    table_start = """
    <table>
        <tbody>
    """

    end_it = """
            </td>
        </tr>
    """

    username = """
    <tr>
        <td>
            <label for="username">Username</label>
        </td>
        <td>
            <input name="username" value='"""+ username_input +"""'>
    """

    if posted == 1 and valid_username(username_input) == None:
        username += """
        <span>Username is not valid</span>
        """

    password = """
    <tr>
        <td>
            <label for="password">Password</label>
        </td>
        <td>
            <input name="password" type="password" value='""" + password_input +"""'>
    """

    if posted == 1 and valid_password(password_input) != None:
        if password_input != verify_password_input:
            password += """
            <span> Password and verify password must be the same </span>
            """
    if posted == 1 and valid_password(password_input) == None:
        password += """
        <span> Password is not valid </span>
        """

    verify_password = """
    <tr>
        <td>
            <label for="verify_password">Verify <br> Password</label>
        </td>
        <td>
            <input name="verify_password" type="password" value='"""+ verify_password_input +"""'/>
    """

    if posted == 1 and valid_password(verify_password_input) != None:
        if password_input != verify_password_input:
            verify_password += """
            <span> Password and verify password must be the same </span>
            """
    if posted == 1 and valid_password(verify_password_input) == None:
        verify_password += """
        <span> Verify Password is not valid </span>
        """

    email = """
        <tr>
            <td>
                <label for="email">Email <br> (optional) </label>
            </td>
            <td>
                <input name="email" type="text" value='""" + email_input + """'>
    """
    if len(email_input) > 0:
        if posted == 1 and valid_email(email_input) == None:
                email += """
                <span> Email is not valid </span>
                """

    table_end = """
        </tbody>
    </table>
    """

    submitbutton = """
    <input type="submit">
    </form>
    """

    page = header + formpost + table_start + username + end_it + password + end_it + verify_password + end_it + email + end_it + table_end + submitbutton
    return page

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(pagebuild("","","","",0))

    def post(self):
        username = (self.request.get("username"))
        password = (self.request.get("password"))
        verify_password = (self.request.get("verify_password"))
        email = (self.request.get("email"))

        if valid_username(username) != None and valid_password(password) != None and password == verify_password:
            if len(email) == 0:
                self.redirect('/Success?username=' + urllib.quote(username))
            elif len(email) > 0 and valid_email(email) != None:
                self.redirect('/Success?username=' + urllib.quote(username))
            else:
                self.response.write(pagebuild(username, password, verify_password,email,1))
        else:
            self.response.write(pagebuild(username, password, verify_password,email,1))

class Sucess(webapp2.RequestHandler):
    def get(self):
        username = (self.request.get("username"))

        self.response.write("<h1>Suckcess"+ " " + cgi.escape(username) +"</h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Success', Sucess),
], debug=True)
