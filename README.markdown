django-maid
=======================

Your app's a mess, but the Django maid can help! Django maid gets rid of
files that have been orphaned—either because their models have been deleted or
because they've been replaced with newer versions. No more messy media
directories while the django maid's on the job!

Installation
------------

1. `pip install -e git+https://github.com/matthewwithanm/django-maid.git#egg=django-maid`
2. Add `maid` to `INSTALLED_APPS` in settings.py.

Usage
--------

    from myapp.models import MyModel
    import maid
    
    maid.register_file_fields(MyModel, 'document', 'thumbnail_image')


Maid will now automatically delete files stored in the `document` and
`thumbnail_image` properties of `MyModel` when they're orphaned.

Warning
--------

If you have a non-standard setup where files are shared between different
models, you should manage the deletion of files yourself. Django-maid can't
tell that the file is being used somewhere else, so she might throw out
something that you didn't want her to.
