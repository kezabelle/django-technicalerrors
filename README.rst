django-technicalerrors
======================

:author: Keryn Knight
:version: 0.1.0

A reusable `Django`_ application which provides alternate templates for the error
pages shown when `DEBUG = True`

Why though?
-----------

Once upon a time, when the web was younger and simpler, I was a web designer. Times changed, the world of frontend exploded and things have changed enough that I'm not super familiar with things like `Tailwind`_, nor as familar with `TypeScript`_ as I'd like.

To a degree then, this is just a toy repository for me to explore `Tailwind`_ and
to a lesser extent, `TypeScript`_.

Along the way, I may produce screens which are *subjectively* better than those
currently bundled with `Django`_, whose error pages have largely stood still (and arguably stood the test of time) since
**2005**.

Goals
-----

- Maintain the same level of information the current debug pages have (because
  that's all the context data I have).
- Responsive.
- Clarity of information. If it's harder to see the information, well, job failed.
- Accessible. Mostly because I don't know as much about modern a11y as I should.
- Ideally, reader mode friendly. I'm not sure how achievable that is, but it'd
  be super nice if the extraneous visuals *could* be stripped away by the browser.

Non-goals
---------

- TODO :)

Targets
-------

- Technical 404 page
- Technical 500 page
- ... others?

Screenshots
-----------

These are heavily work-in-progress, as I think through the various bits...

500 (Server Error)
^^^^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/kezabelle/django-technicalerrors/main/images/500.png
   :alt: technical 500 page
   :width: 400px
   :align: left
   :target: https://raw.githubusercontent.com/kezabelle/django-technicalerrors/main/images/500.png


404 (Not found)
^^^^^^^^^^^^^^^^^^

.. image:: https://raw.githubusercontent.com/kezabelle/django-technicalerrors/main/images/404.png
   :alt: technical 404 page
   :width: 400px
   :align: left
   :target: https://raw.githubusercontent.com/kezabelle/django-technicalerrors/main/images/404.png


Notes
-----

There's a number of differences between the data given to the 500 and 404 pages, which I'd need to get fixed upstream to be consistent, but that's likely a hard sell if they're not *used* ...

- Unfortunately, the context given to the **404** page doesn't include any of the following:

  - The Django version (e.g. ``4.0.1``)
  - The Python version (e.g. ``3.9.5``)
  - The server time (e.g. ``Fri, 21 Jan 2022 20:47:51 +0000``)
  - The frame which caused the ``Http404`` to be thrown.


.. _Django: https://docs.djangoproject.com/
.. _Tailwind: https://tailwindcss.com/
.. _TypeScript: https://www.typescriptlang.org/
