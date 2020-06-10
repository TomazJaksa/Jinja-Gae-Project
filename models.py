from google.appengine.ext import ndb

class Narocilo(ndb.Model):
    ime = ndb.StringProperty()
    priimek = ndb.StringProperty()
    email = ndb.StringProperty()
    izdelek = ndb.StringProperty()
    opombe = ndb.TextProperty()
    datumVnosa = ndb.DateTimeProperty(auto_now_add = True)


class Izdelek(ndb.Model):
    slika = ndb.StringProperty()
    cena = ndb.FloatProperty()
    tip = ndb.StringProperty()
    ime = ndb.StringProperty()
    opis = ndb.StringProperty()
    datumVnosa = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)

class Blog(ndb.Model):
    slika = ndb.StringProperty()
    naslov = ndb.StringProperty()
    povzetek = ndb.StringProperty()
    polnClanek = ndb.TextProperty()
    bloger = ndb.TextProperty()
    datumVnosa = ndb.DateTimeProperty(auto_now_add=True)
    izbrisan = ndb.BooleanProperty(default=False)