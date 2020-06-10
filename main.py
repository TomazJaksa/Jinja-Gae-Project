from google.appengine.api import users
#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Narocilo, Izdelek, Blog

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}

        # we'll put google login code here, so it gets automatically used in every handler.
        user = users.get_current_user()
        params["user"] = user

        if user:
            logged_in = True
            logout_url = users.create_logout_url('/')
            params["logout_url"] = logout_url
        else:
            logged_in = False
            login_url = users.create_login_url('/')
            params["login_url"] = login_url

        params["logged_in"] = logged_in

        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):

        return self.render_template("hello.html")

class UrskaHandler(BaseHandler):
    def get(self):
        return self.render_template("urska.html")

class KatalogHandler(BaseHandler):
    def get(self):
        return self.render_template("katalog.html")

class UhaniHandler(BaseHandler):
    def get(self):
        seznamUhanov = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamUhanov}
        return self.render_template("uhani.html", params)

class PriponkeHandler(BaseHandler):
    def get(self):
        seznamPriponk = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamPriponk}
        return self.render_template("priponke.html", params)

class ObeskiHandler(BaseHandler):
    def get(self):
        seznamObeskov = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamObeskov}
        return self.render_template("obeski.html", params)

class OgrliceHandler(BaseHandler):
    def get(self):
        seznamOgrlic = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamOgrlic}
        return self.render_template("ogrlice.html", params)

class PrstaniHandler(BaseHandler):
    def get(self):
        seznamPrstanov = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamPrstanov}
        return self.render_template("prstani.html", params)

class ZapestniceHandler(BaseHandler):
    def get(self):
        seznamZapestnic = Izdelek.query(Izdelek.izbrisan == False).fetch()
        params = {"izdelki": seznamZapestnic}
        return self.render_template("zapestnice.html", params)

class BlogHandler(BaseHandler):
    def get(self):
        seznamBlogov = Blog.query(Blog.izbrisan == False).fetch()
        params = {"blogi": seznamBlogov}
        return self.render_template("blog.html",params)

class VsakBlogHandler(BaseHandler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        params = {"blog":blog}
        return self.render_template("posamezenBlog.html",params)

class DodajBlogHandler(BaseHandler):
    def post(self):
        slika = self.request.get("slika")
        naslov = self.request.get("naslov")
        povzetek = self.request.get("povzetek")
        polnClanek = self.request.get("polnClanek")
        bloger = self.request.get("bloger")

        blog = Blog(slika=slika, naslov=naslov, povzetek=povzetek, polnClanek=polnClanek, bloger=bloger)
        blog.put()

        return self.redirect_to("seznamBlogov")

class UrediBlogHandler(BaseHandler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        params = {"blog": blog}

        return self.render_template("urediBlog.html", params=params)

    def post(self, blog_id):
        slika = self.request.get("slika")
        naslov = self.request.get("naslov")
        povzetek = self.request.get("povzetek")
        polnClanek = self.request.get("polnClanek")
        bloger = self.request.get("bloger")

        blog = Blog.get_by_id(int(blog_id))

        blog.slika = slika
        blog.naslov = naslov
        blog.povzetek = povzetek
        blog.polnClanek = polnClanek
        blog.bloger = bloger

        blog.put()

        return self.redirect_to("seznamBlogov")

class UrediIzdelekHandler(BaseHandler):
    def get(self, izdelek_id):
        izdelek = Izdelek.get_by_id(int(izdelek_id))
        params = {"izdelek": izdelek, "checked": "checked" }
        return self.render_template("urediIzdelek.html", params)

    def post(self, izdelek_id):
        slika = self.request.get("slika")
        cena = float(self.request.get("cena"))
        tip = self.request.get("tip")
        ime = self.request.get("ime")
        opis = self.request.get("opis")

        izdelek = Izdelek.get_by_id(int(izdelek_id))

        izdelek.slika = slika
        izdelek.cena = cena
        izdelek.tip = tip
        izdelek.ime = ime
        izdelek.opis = opis
        izdelek.put()

        return self.redirect_to("katalogIzdelkov")

class IzbrisiIzdelekHandler(BaseHandler):
    def get(self, izdelek_id):
        izdelek = Izdelek.get_by_id(int(izdelek_id))
        params = {"izdelek": izdelek}

        return self.render_template("izbrisIzdelka.html", params)

    def post(self, izdelek_id):
        izdelek = Izdelek.get_by_id(int(izdelek_id))
        izdelek.izbrisan = True
        izdelek.put()
        #izdelek.key.delete()
        return self.redirect_to("katalogIzdelkov")

class IzbrisiBlogHandler(BaseHandler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        params = {"blog": blog}

        return self.render_template("izbrisBloga.html", params)

    def post(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        blog.izbrisan=True
        blog.put()
        #blog.key.delete()
        return self.redirect_to("seznamBlogov")

class SeznamIzbrisanihHandler(BaseHandler):
    def get(self):
        seznamIzbrisanihBlogov = Blog.query(Blog.izbrisan == True).fetch()
        seznamIzbrisanihIzdelkov = Izdelek.query(Izdelek.izbrisan == True).fetch()

        params = {"izdelki": seznamIzbrisanihIzdelkov, "blogi":seznamIzbrisanihBlogov}

        return self.render_template("seznamIzbrisanih.html", params)

class ObnoviIzdelekHandler(BaseHandler):
    def get(self, izdelek_id):
        izdelek = Izdelek.get_by_id(int(izdelek_id))
        params = {"izdelek": izdelek}

        return self.render_template("obnoviIzdelek.html", params)

    def post(self, izdelek_id):
        izdelek = Izdelek.get_by_id(int(izdelek_id))
        izdelek.izbrisan=False
        izdelek.put()

        return self.redirect_to("katalogIzdelkov")

class ObnoviBlogHandler(BaseHandler):
    def get(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        params = {"blog": blog}

        return self.render_template("obnoviBlog.html", params)

    def post(self, blog_id):
        blog = Blog.get_by_id(int(blog_id))
        blog.izbrisan=False
        blog.put()

        return self.redirect_to("seznamBlogov")

class RezultatHandler(BaseHandler):
    def post(self):
        rezultat = self.request.get("vnos")
        slika = self.request.get("slika")

        sporocilo = Narocilo(vnos=rezultat, slika=slika)
        sporocilo.put()

        return self.render_template("uhani.html")

class NarocilaHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()
        params = {"seznam":seznam}
        return self.render_template("narocila.html",params)

class NarociloHandler(BaseHandler):
    def get(self, narocilo_id):
        narocilo = Sporocilo.get_by_id(int(narocilo_id))
        params = {"narocilo":narocilo}
        return self.render_template("narocilo.html",params)

class DodajIzdelekHandler(BaseHandler):

    def post(self):
        slika = self.request.get("slika")
        cena = float(self.request.get("cena"))
        tip = self.request.get("tip")
        ime = self.request.get("ime")
        opis = self.request.get("opis")

        izdelek = Izdelek(slika=slika, cena=cena, tip= tip, ime=ime, opis=opis)
        izdelek.put()

        return self.redirect_to("katalogIzdelkov")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/dodajIzdelek', DodajIzdelekHandler),
    webapp2.Route("/urska", UrskaHandler),
    webapp2.Route("/blog", BlogHandler, name="seznamBlogov"),
    webapp2.Route("/blog/<blog_id:\d+>", VsakBlogHandler),
    webapp2.Route('/urediBlog/<blog_id:\d+>', UrediBlogHandler),
    webapp2.Route("/izbrisiBlog/<blog_id:\d+>", IzbrisiBlogHandler),
    webapp2.Route("/dodajBlog", DodajBlogHandler),
    webapp2.Route("/katalog",KatalogHandler, name="katalogIzdelkov"),
    webapp2.Route("/uhani", UhaniHandler),
    webapp2.Route("/priponke", PriponkeHandler),
    webapp2.Route("/obeski", ObeskiHandler),
    webapp2.Route("/ogrlice", OgrliceHandler),
    webapp2.Route("/prstani", PrstaniHandler),
    webapp2.Route("/zapestnice", ZapestniceHandler),
    webapp2.Route("/urediIzdelek/<izdelek_id:\d+>", UrediIzdelekHandler),
    webapp2.Route("/izbrisiIzdelek/<izdelek_id:\d+>", IzbrisiIzdelekHandler),
    webapp2.Route("/obnovi", SeznamIzbrisanihHandler),
    webapp2.Route("/obnoviIzdelek/<izdelek_id:\d+>", ObnoviIzdelekHandler),
    webapp2.Route("/obnoviBlog/<blog_id:\d+>", ObnoviBlogHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route("/narocila", NarocilaHandler),
    webapp2.Route("/narocilo/<narocilo_id:\d+>", NarociloHandler)
], debug=True)
