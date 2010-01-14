# LingDesktop: 
#
#Copyright (C) 2010 LingDesktop Project
#     Author:       Scott Farrar <farrar@uw.edu>
#                   Dwight van Tuyl <dvantuyl@uw.edu> 
#     URL: <http://purl.org/linguistics/lingdeskop>
#     For license information, see LICENSE.txt




import os
# Django settings for lingdesktop project.

DEBUG = True 
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_ENGINE = 'mysql'
#DATABASE_NAME = 'GOLDComm'             # Or path to database file if using sqlite3.
DATABASE_NAME = 'lingdesktop_db'             # Or path to database file if using sqlite3.

#DATABASE_USER = 'farrar'             # Not used with sqlite3.
#DATABASE_USER = 'root'             # Not used with sqlite3.
#DATABASE_PASSWORD = 'akellica'         # Not used with sqlite3.
#DATABASE_PASSWORD = ';lkjJK'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = '/home2/farrar/e-linguistics/dev/lingdesktop/htdocs/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
#MEDIA_URL = 'http://uakari.ling.washington.edu/e-linguistics/dev/lingdesktop/htdocs/'

#MEDIA_URL = '/media/'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
#print PROJECT_PATH


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/adminmedia/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3@o*b+t)yo41cfcu65upmx+b-hfw4st=uu7l@esixbv1a)0vo='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'lingdesktop.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'/home2/farrar/e-linguistics/dev/lingdesktop/templates/',
    #'/home2/farrar/e-linguistics/dev/lingdesktop/templates/termseteditor/',
    os.path.join(PROJECT_PATH, '../templates/')

    )


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    #'lingdesktop.termseteditor',
    'lingdesktop.search',
)

FIXTURE_DIRS = (
            
    os.path.join(PROJECT_PATH, '/search/fixtures/')
)
