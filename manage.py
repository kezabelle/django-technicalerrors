import os
import sys
from datetime import datetime
from tempfile import gettempdir

import django
from django.conf import settings
from django.http import HttpResponse, Http404
from django.urls import path, re_path, include
from django.template.loader import select_template
from django.template import Template, Context

HAS_JINJA = False
HAS_PATTERNLIBRARY = False
HAS_LIVERELOADISH = False
HAS_SHOUTY_TEMPLATES = False

try:
    import jinja2
    HAS_JINJA = True
except ModuleNotFoundError:
    sys.stderr.write("`jinja2` is necessary for this demo project")
    sys.exit(1)


EXTRA_INSTALLED_APPS = ()
EXTRA_MIDDLEWARE = ()

USE_TECHNICALERRORS = os.environ.get("USE_TECHNICALERRORS", "1").lower() in {
    "1",
    "t",
    "true",
    "ok",
    "yes",
}
if USE_TECHNICALERRORS:
    EXTRA_INSTALLED_APPS += ("technicalerrors.TechnicalErrors",)

try:
    from livereloadish import watch_file

    EXTRA_INSTALLED_APPS += ("livereloadish",)
    EXTRA_MIDDLEWARE += ("livereloadish.middleware.LivereloadishMiddleware",)
    HAS_LIVERELOADISH = True
except ModuleNotFoundError:
    pass

try:
    import pattern_library

    EXTRA_INSTALLED_APPS += ("pattern_library.apps.PatternLibraryAppConfig",)
    HAS_PATTERNLIBRARY = True
except ModuleNotFoundError:
    pass

try:
    import shouty
    # TODO: set this up and make sure the contexts are good.
    # EXTRA_INSTALLED_APPS += ("shouty.Shout",)
    HAS_SHOUTY_TEMPLATES = True
except ModuleNotFoundError:
    pass


HERE = os.path.abspath(os.path.dirname(__file__))


if not settings.configured:
    settings.configure(
        SECRET_KEY="??????????????????????????????????????????????????????????",
        DEBUG=True,
        INSTALLED_APPS=(
            "django.contrib.staticfiles",
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.messages",
            "django.contrib.sessions",
            "django.contrib.admin",
            "django.contrib.admindocs",
        )
        + EXTRA_INSTALLED_APPS,
        ALLOWED_HOSTS=("*"),
        ROOT_URLCONF=__name__,
        MIDDLEWARE=(
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        )
        + EXTRA_MIDDLEWARE,
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": (os.path.join(HERE, "extra_templates"),),
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": (
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ),
                    "builtins": ["pattern_library.loader_tags"] if HAS_PATTERNLIBRARY else [],
                },
            },
            {
                "BACKEND": "django.template.backends.jinja2.Jinja2",
                "DIRS": [os.path.join(HERE, "extra_templates")],
                "APP_DIRS": True,
                "OPTIONS": {
                    "environment": "jinja2.Environment",
                    # Not recommended, but supported
                    "context_processors": (
                        "django.template.context_processors.request",
                        "django.contrib.messages.context_processors.messages",
                    ),
                },
            },
        ],
        LOGGING={
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "livereloadish": {
                    "handlers": ["console"],
                    "level": "WARNING",
                    "propagate": False,
                },
                "django.template": {
                    "handlers": ["console"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        },
        STATIC_URL="/static/",
        USE_I18N=True,
        USE_TZ=True,
        TIME_ZONE="UTC",
        X_FRAME_OPTIONS="SAMEORIGIN",
        PATTERN_LIBRARY={
            "SECTIONS": (
                ("components", ["patterns/components"]),
                ("pages", ["patterns/pages"]),
            ),
            "TEMPLATE_SUFFIX": ".html",
            "PATTERN_BASE_TEMPLATE_NAME": "patterns/base.html",
            "BASE_TEMPLATE_NAMES": ["patterns/base_page.html"],
        },
    )
    django.setup()

from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls


def demo404(request, *args, **kwargs) -> HttpResponse:
    raise Http404("Custom message")


def demo404_with_long_message(request, *args, **kwargs) -> HttpResponse:
    raise Http404("Ruined"*50)


def nested3():
    filename = os.path.join(
        gettempdir(),
        "a_long_path",
        "that_probably",
        "goes_off_screen",
        "and_causes_wrapping_issues",
        "elsewhere",
        "on_the_page",
        "that_need_addressing",
        "a_random_file_that_shouldnt_exist.mp3",
    )
    with open(filename, "rb") as f:
        return f.read()


def nested2():
    a = 1
    b = {1, 2, 3}
    c = (1, 2, 3)
    a_really_long_variable_name = 4
    nested_var = {"a": a, "b": b, "c": c}
    a_really_long_variable_value = "Ruined" * 50
    try:
        return nested3()
    except ZeroDivisionError as exc:
        raise ValueError("Ruined")
    except FileNotFoundError as exc:
        raise TypeError(
            "RuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuinedRuined"
        ) from exc


def nested1():
    nested_var = datetime.utcnow()
    return nested2()


def nested():
    nested_var = 1
    return nested1()


def demo500(request) -> None:
    var = nested()


def demo500templatemissing(request):
    return select_template(("demo/a.html", "demo/b.html", "demo/c.html", "demo/d.html"))


def demo500templatesyntax(request):
    return Template(
        """Line 1
    More lines go here
    and then some
    and soon we'll maybe get to the error?
    Nah let's keep going
    Here's some HTML to keep us going
    <br>
    <br>
    <br>
    <br>
    Go away, line 1!
    Example template {{ 'syntax'|bad_filter }} some really long line error that might cause issues on small screens
    Ok now we've done the error
    How much more do we show afterwards?
    Got to be a few lines right?
    Probably...
    5 or 10 maybe?
    Looks like 10, so onwards we go...
    At some point the EOF will get cut off.
    But not yet, lines aplenty
    Keep it up, nearly there
    One more line perhaps? Boom there it is.
    EOF"""
    )


def demo500unicodeencode(request):
    "????????????????????".encode("ascii")


def demo500unicodedecode(request):
    b"\xf0\x9f\xa4\x9e\xf0\x9f\x98\xa1\xf0\x9f\xa4\xac\xf0\x9f\x91\x8a\xf0\x9f\x98\x94".decode(
        "ascii"
    )

from django.template.response import TemplateResponse

def index(request):
    class PatchedTemplate(Template):
        def render(self, context, request=None):
            return super().render(context=context)

    return TemplateResponse(request, PatchedTemplate("""
    <!DOCTYPE html><html lang="en"><body>
    <ul>
    <li><a href="{% url 'demo500' %}">Example 500</a>
    <li><a href="{% url 'nested_appname:unicodes:demo500unicodedecode' %}">Example 500 #2 (string decoding)</a>
    <li><a href="{% url 'nested_appname:unicodes:demo500unicodeencode' %}">Example 500 #3 (string encoding)</a>
    <li><a href="{% url 'nested_appname:demo500templatesyntax' %}">Example 500 #3 (template syntax)</a>
    <li><a href="{% url 'nested_appname:demo500templatemissing' %}">Example 500 #4 (template missing)</a>
    <li><a href="{% url 'demo404' %}">Example 404</a>
    <li><a href="{% url 'demo404_with_value_arg' '100' %}">Example 404 #2</a>
    <li><a href="{% url 'demo404_with_any_args' 'example' %}">Example 404 #3</a>
    <li><a href="{% url 'demo404_ruined' %}">Example 404 #4</a>
    <li><a href="/not_a_url">Example 404 #5</a>
    <li><a href="/500/unicode/not_a_url">Example 404 #6</a>
    </ul>
    {{ something.goes.here }}
    </body></html>
    """), Context({'something': {'goes': {}}}))



urlpatterns = [
    path("admin/docs/", include(admindocs_urls)),
    path("admin/", admin.site.urls),
    re_path("^404/" + '_'.join(['ruined']*30), demo404_with_long_message, name="demo404_ruined"),
    path("404/<int:value>", demo404, name="demo404_with_value_arg"),
    re_path("^404/(.+)", demo404, name="demo404_with_any_args"),
    path("404", demo404, name="demo404"),
    path(
        "500/",
        include(
            (
                [
                    re_path(
                        "^unicode/",
                        include(
                            (
                                [
                                    path(
                                        "decode",
                                        demo500unicodedecode,
                                        name="demo500unicodedecode",
                                    ),
                                    path(
                                        "encode",
                                        demo500unicodeencode,
                                        name="demo500unicodeencode",
                                    ),
                                ],
                                "unicodes",
                            )
                        ),
                    ),
                    path(
                        "inucedo/other_path",
                        demo500unicodedecode,
                        name="same_length_as_unicode",
                    ),
                    path(
                        "template/syntax",
                        demo500templatesyntax,
                        name="demo500templatesyntax",
                    ),
                    path(
                        "template/missing",
                        demo500templatemissing,
                        name="demo500templatemissing",
                    ),
                ],
                "nested_appname",
            )
        ),
    ),
    path("500", demo500, name="demo500"),
    path("", index, name="index"),
]
if HAS_PATTERNLIBRARY:
    urlpatterns += [
        path("pattern-library/", include("pattern_library.urls")),
    ]


if __name__ == "__main__":
    from django.core import management

    management.execute_from_command_line()
else:
    from django.core.wsgi import get_wsgi_application

    application = get_wsgi_application()
