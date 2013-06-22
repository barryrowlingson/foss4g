# 
import os
from django.conf.global_settings import (TEMPLATE_CONTEXT_PROCESSORS,
    STATICFILES_FINDERS)

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
PROJECT_NAME = os.path.split(PROJECT_ROOT)[-1]

DEBUG = TEMPLATE_DEBUG = False
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

ADMINS = (
    ('Barry Rowlingson', 'b.rowlingson@gmail.com'),
)
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = '[%s] ' % PROJECT_NAME

DEFAULT_FROM_EMAIL = 'info@2013.foss4g.org'
SERVER_EMAIL = 'info@2013.foss4g.org'

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en'

USE_I18N = True
USE_L10N = True

SITE_ID = 1

ugettext = lambda s: s
LANGUAGES = (
    ('en', 'English'),
)

MEDIA_URL = '/site_media/'
STATIC_URL = '/static_media/'
ADMIN_MEDIA_PREFIX = '/static_media/admin/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static_media'),
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)

STATICFILES_FINDERS += (
    'pyconde.helpers.static.AppMediaDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_CSS_FILTERS = (
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
)

COMPRESS_PRECOMPILERS = (
   ('text/less', 'lessc -x {infile} {outfile}'),
)

ROOT_URLCONF = '%s.urls' % PROJECT_NAME

INSTALLED_APPS = [
    # Skins

    'pyconde.skins.foss4g',
    'pyconde.skins.default',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'crispy_forms',
    'south',
    'easy_thumbnails',
    'filer',
    'compressor',
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'userprofiles',
    'userprofiles.contrib.accountverification',
    'userprofiles.contrib.emailverification',
    'userprofiles.contrib.profiles',
    'taggit',
    'debug_toolbar',
    'helpdesk',
    'haystack',
    'tinymce', # If you want tinymce, add it in the settings.py file.
    'django_gravatar',

    'cms.plugins.inherit',
    'cms.plugins.googlemap',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.twitter',
    'cms.plugins.text',
    'cmsplugin_filer_image',
    'cmsplugin_news',

    # Symposion apps
    'pyconde.conference',
    'pyconde.speakers',
    'pyconde.proposals',
    'pyconde.sponsorship',

    # Custom apps
    'pyconde.accounts',
    'pyconde.attendees',
    'pyconde.events',
    'pyconde.reviews',
    'pyconde.schedule',
    'pyconde.search',
    'pyconde.helpers',

    # foss4g booking
    'pyconde.booking',

    # my programme code
    'pyconde.programme',
]

MIDDLEWARE_CLASSES = [
    'pyconde.helpers.middleware.CorrectDomainMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    #'cms.middleware.toolbar.ToolbarMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'sekizai.context_processors.sekizai',
    'pyconde.conference.context_processors.current_conference',
    'pyconde.reviews.context_processors.review_roles',
    'pyconde.context_processors.less_settings',
)

# TEMPLATE_DIRS = (
#     os.path.join(PROJECT_ROOT, 'skins', 'default'),
#     os.path.join(PROJECT_ROOT, 'skins', 'pyconde2012'),
# )

USERPROFILES_CHECK_UNIQUE_EMAIL = True
USERPROFILES_DOUBLE_CHECK_EMAIL = False
USERPROFILES_DOUBLE_CHECK_PASSWORD = True
USERPROFILES_REGISTRATION_FULLNAME = True
USERPROFILES_USE_ACCOUNT_VERIFICATION = True
USERPROFILES_USE_PROFILE = True
USERPROFILES_INLINE_PROFILE_ADMIN = True
USERPROFILES_USE_PROFILE_VIEW = False
USERPROFILES_REGISTRATION_FORM = 'pyconde.accounts.forms.ProfileRegistrationForm'
USERPROFILES_PROFILE_FORM = 'pyconde.accounts.forms.ProfileForm'
USERPROFILES_EMAIL_VERIFICATION_DONE_URL = 'userprofiles_profile_change'

AUTH_PROFILE_MODULE = 'accounts.Profile'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

CMS_TEMPLATES = (
    ('cms/default.html', 'Default template'),
    ('cms/frontpage.html', 'Frontpage template'),
    ('cms/page_templates/fullpage.html', 'Full page width (schedule, ...)'),
)

CMS_LANGUAGE_FALLBACK = False
CMS_MENU_TITLE_OVERWRITE = True
CMS_REDIRECTS = True
CMS_SHOW_START_DATE = False
CMS_SHOW_END_DATE = False
CMS_MODERATOR = False
CMS_SEO_FIELDS = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_SIZE = 100

WYM_TOOLS = ",\n".join([
    "{'name': 'Bold', 'title': 'Strong', 'css': 'wym_tools_strong'}",
    "{'name': 'Italic', 'title': 'Emphasis', 'css': 'wym_tools_emphasis'}",
    "{'name': 'Superscript', 'title': 'Superscript', 'css': 'wym_tools_superscript'}",
    "{'name': 'Subscript', 'title': 'Subscript', 'css': 'wym_tools_subscript'}",
    "{'name': 'InsertOrderedList', 'title': 'Ordered_List', 'css': 'wym_tools_ordered_list'}",
    "{'name': 'InsertUnorderedList', 'title': 'Unordered_List', 'css': 'wym_tools_unordered_list'}",
    "{'name': 'Indent', 'title': 'Indent', 'css': 'wym_tools_indent'}",
    "{'name': 'Outdent', 'title': 'Outdent', 'css': 'wym_tools_outdent'}",
    "{'name': 'Undo', 'title': 'Undo', 'css': 'wym_tools_undo'}",
    "{'name': 'Redo', 'title': 'Redo', 'css': 'wym_tools_redo'}",
    "{'name': 'Paste', 'title': 'Paste_From_Word', 'css': 'wym_tools_paste'}",
    "{'name': 'ToggleHtml', 'title': 'HTML', 'css': 'wym_tools_html'}",
    "{'name': 'CreateLink', 'title': 'Link', 'css': 'wym_tools_link'}",
    "{'name': 'Unlink', 'title': 'Unlink', 'css': 'wym_tools_unlink'}",
    "{'name': 'InsertImage', 'title': 'Image', 'css': 'wym_tools_image'}",
    "{'name': 'InsertTable', 'title': 'Table', 'css': 'wym_tools_table'}",
    "{'name': 'Preview', 'title': 'Preview', 'css': 'wym_tools_preview'}",
])

CMSPLUGIN_NEWS_FEED_TITLE = u'FOSS4G 2013-News'
CMSPLUGIN_NEWS_FEED_DESCRIPTION = u'FOSS4G 2013 Nottingham News'
CONFERENCE_ID = 1

ATTENDEES_CUSTOMER_NUMBER_START = 20000
ATTENDEES_PRODUCT_NUMBER_START = 1000

PROPOSALS_SUPPORT_ADDITIONAL_SPEAKERS = True
PROPOSALS_TYPED_SUBMISSION_FORMS = {
    'tutorial': 'pyconde.proposals.forms.TutorialSubmissionForm',
    'talk': 'pyconde.proposals.forms.TalkSubmissionForm',
}
PROPOSAL_LANGUAGES = (
    ('en', ugettext('English')),
)

LESS_USE_DYNAMIC_IN_DEBUG = True

# Django Helpdesk stuff
#
#   Configuration is done in admin,
#   but these placeholders are required in order to make it work

QUEUE_EMAIL_BOX_TYPE = None
QUEUE_EMAIL_BOX_HOST = None
QUEUE_EMAIL_BOX_USER = None
QUEUE_EMAIL_BOX_SSL = None
QUEUE_EMAIL_BOX_PASSWORD = None

SCHEDULE_CACHE_SCHEDULE = True

# Search configuration
#    If no other search backend is specified, Whoosh is used to make the setup
#    as simple as possible. In production we will be using a Lucene-based
#    backend like SOLR or ElasticSearch.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index'),
        'STORAGE': 'file',
        'INCLUDE_SPELLING': True,
        'BATCH_SIZE': 100,
    }
}

# Disable south migrations during unittests
SOUTH_TESTS_MIGRATE = False

#'advlist autolink link image lists charmap print preview'
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'style_formats': [
        {"title": 'Code', "inline": 'code'},
        {"title": 'Small caps', "inline": 'span', "styles": {"font-variant": 'small-caps', "text-transform": 'capitalize'}}], 
    'plugins': "table,lists,advlink,wordcount", #table,spellchecker,paste,searchreplace",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    "theme_advanced_buttons1" : "styleprops,styleselect,forecolor,backcolor,bold,italic,underline,code,formatselect",
    "theme_advanced_buttons2" : "bullist,numlist,separator,outdent,indent,separator,undo,redo,separator,link,unlink,separator,hr,removeformat,visualaid,separator,sub,sup,separator,charmap",
    'theme_advanced_resizing': True,
}

# TINYMCE_DEFAULT_CONFIG={
#     'theme': 'advanced',
#     'relative_urls': False,
#     'theme_advanced_resizing': True,
# }

ACCOUNTS_FALLBACK_TO_GRAVATAR = True

# For Elasticsearch you can use for instance following configuration in your
# settings.py.
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'pyconde.search.backends.elasticsearch.Engine',
#         'URL': 'http://127.0.0.1:9200/',
#         'INDEX_NAME': 'pyconde2013',
#     }
# }

# set this in your settings.py to obscure some URLs and don't 
# check that file into a public repo

# this happens here so that urls.py files that use it don't barf if you don't set
# it
import string
import random
OBSCURE = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))

