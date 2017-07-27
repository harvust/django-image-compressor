Django Image Compressor
=======================

Django Image Compressor is a tool for optimizing your website's static images for serving in production. Django Image Compressor
alters the :code:`staticfiles.json` manifest generated after running :code:`collectstatic` by changing the image mapping to
the new optimized images located in a directory in :code:`STATIC_ROOT`.


Installation
------------

::

    pip install django-image-compressor


Getting started
---------------

Add to :code:`INSTALLED_APPS`

::

    INSTALLED_APPS = [
        # some other apps...
        'imagecompressor'
    ]

Run :code:`collectstatic`

::

    python manage.py collectstatic

Run :code:`compressimages`

::

    python manage.py compressimages


**Positional arguments**

:code:`path`
    The path relative to :code:`STATIC_ROOT`, or app name, whose images you want compressed.


**Optional Arguments**
  --optimize            If present and true, indicates that the encoder should
                        make an extra pass over the image in order to select
                        optimal encoder settings.
  --quality QUALITY     The image quality, on a scale from 1 (worst) to 95
                        (best).
  --progressive         If present and true, indicates that this image should
                        be stored as a progressive JPEG file.
  --lossless            If present and true, instructs the WEBP writer to use
                        lossless compression.

For more information on these options see the  `Pillow documentation. <http://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html>`__

Examples
--------
::

    python manage.py compressimages --optimize --progressive --quality 75

Will optimize all JPG, and PNG files in :code:`STATIC_ROOT`, and make JPGs progressive with quality 75.

::

    python manage.py compressimages polls --progressive

Will make all JPG files in the :code:`polls` app progressive with Pillow defaults for the other parameters. Again see the `Pillow documentation. <http://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html>`__

::

    python manage.py compressimages

This is the first example in "Getting started". It will not modify the images at all, instead it will rename them and place them in a new directory in :code:`STATIC_ROOT`.

Settings
--------
:IMAGE_COMPRESS_ROOT:
    This is the name of the directory images will be placed in after running :code:`compressimages` (Default: 'IMAGES').