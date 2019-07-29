import os
import webapp2
import jinja2


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

from google.appengine.ext import ndb
from google.appengine.api import users

def handleEmergency(person):
    template_vars = {
        "person": person,
    }
    template = jinja_env.get_template("templates/emergency.html")
    return template.render(template_vars)

class Information(ndb.Model):
    name = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    number = ndb.StringProperty(required=True)
    contact = ndb.StringProperty(required=False)
    function= ndb.StringProperty(required=False)

class Person(ndb.Model):
    id = ndb.StringProperty(required=True)
    eservice_info = ndb.KeyProperty(repeated=True)
    econtacts_info = ndb.StructuredProperty(Information,repeated=True)


class mainPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        logout_link = users.create_logout_url('/setup')
        template_vars = {
            "current_user": current_user,
            "logout_link": logout_link,
        }
        template = jinja_env.get_template("templates/hello.html")
        self.response.write(template.render(template_vars))

class emergencyPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        person = Person.query().filter(Person.id == current_user.email()).fetch()
        if len(person) == 0:
            template = jinja_env.get_template("templates/block.html")
            self.response.write(template.render())
        else:
            self.response.write(handleEmergency(person[0]))

class setupPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user().email()
        person = Person.query().filter(Person.id == current_user).fetch()
        if len(person) == 0:
            template = jinja_env.get_template("templates/setup.html")
            self.response.write(template.render())
        else:
            template = jinja_env.get_template("templates/repeat.html")
            self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user().email()
        police_info = Information(
            name="Police Department",
            location=self.request.get("Country")+":"+self.request.get("City")+":"+self.request.get("Zip"),
            number=(self.request.get("Police")))
        fire_info = Information(
            name="Fire Department",
            location=self.request.get("Country")+":"+self.request.get("City")+":"+self.request.get("Zip"),
            number=(self.request.get("Fire")))
        contact_info= Information(
            name= "Emergency Contacts",
            contact=self.request.get('contact'),
            number=(self.request.get('contact_num'))
            )
        hotline_info= Information(
            name="Hotline Information",
            function=self.request.get('hotline_function'),
            number=self.request.get('hotline'),
            )
        #check for the existence of duplicates
        Person(id=str(current_user),eservice_info=[police_info.put(),fire_info.put()],econtacts_info=[]).put()
        template = jinja_env.get_template("templates/finished_setup.html")
        self.response.write(template.render())

class contactPage(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user().email()
        person = Person.query().filter(Person.id == current_user).fetch()
        template = jinja_env.get_template("templates/contacts.html")
        self.response.write(template.render())
    def post(self):
        current_user = users.get_current_user().email()
        contact_info= Information(
            name= "Emergency Contacts",
            contact=self.request.get('contact'),
            number=(self.request.get('contact_num'))
            )
        template = jinja_env.get_template("templates/finished_setup.html")
        self.response.write(template.render())
        #.put() the information (also for new vars in setupPage)


class searchPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/search.html")
        self.response.write(template.render())
    def post(self):
        input_location = [self.request.get("Country"),self.request.get("City"),self.request.get("Zip")]
        location = Information.location.split(":")
        for i in range(3):
            test = Information.query().filter(location[i] == input_location[i])
            if len(test.fetch()) == 1:
                self.response.write(handleEmergency(test[0]))
        self.response.write("templates/not_found.html")

<<<<<<< HEAD

=======
class aboutPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/about.html")
        self.response.write(template.render())
>>>>>>> 041a9d035d83441ec7fa4635998f264346f4e956

app = webapp2.WSGIApplication([
    ('/',mainPage),
    ('/emergency',emergencyPage),
    ('/setup',setupPage),
<<<<<<< HEAD
    ('/search',searchPage),
    ('/contacts',contactPage),

=======
<<<<<<< HEAD
    ('/about',aboutPage),
=======
    ('/search',searchPage)
>>>>>>> 96b1b4fccf364abdacc7053a76cf75c99916d7dc
>>>>>>> 041a9d035d83441ec7fa4635998f264346f4e956
    ],debug=True
)
