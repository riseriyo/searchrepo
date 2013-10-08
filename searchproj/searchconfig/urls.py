#****************************************************
# urls.py: like a table of contents for the project;
# mapping of URLs to locations of python callback
# functions in views.py
#****************************************************

# stdlib 
import pdb

# django core
from django.conf.urls import patterns
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
#from django.conf import settings

#*********** DEVELOPMENT --  models to use -- DEVELOPMENT ***********************
from settings.local import STATIC_ROOT
from settings.local import MEDIA_URL
from settings.local import MEDIA_ROOT
from settings.local import DEBUG
# *********************************************************************************

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# 3rd party plugins
from haystack.views import SearchView, FacetedSearchView, search_view_factory
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

# author's code
#from profiles.formsprofilessearch import ProfilesSearchForm, ProfilesHaystackForm

#pdb.set_trace()
urlpatterns = patterns('',
                # Examples:
                # url(r'^$', 'searchapp.views.home', name='home'),
                # url(r'^searchapp/', include('searchapp.foo.urls')),

                # Uncomment the admin/doc line below to enable admin documentation:
                # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                # Uncomment the next line to enable the admin:
                url(r'^admin/', include(admin.site.urls)),

            	# main navigation page
            	url(r'^$', 'profiles.viewsmainnav.home', name='home'),
                url(r'^gallery/$', 'profiles.viewsmainnav.gallery', name='gallery'),
            	url(r'^about/$', 'profiles.viewsmainnav.about', name='about'),

                # search in the default URLconf for Haystack
                url(r'^search/', include('profiles.urls')),
                #url(r'^search/', include('uploads.urls')),
                url(r'^search/', include('haystack.urls')),


                # static files, images; force Django to server static files
                (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_ROOT}),

                # user registration, activation
                url(r'^register/$', 'profiles.viewsregistration.Registration', name='register'),
                url(r'^accounts/confirm/(?P<activation_key>\w+)/$', 'profiles.viewsregistration.confirm'),

                # login, logout, user profile dashboard
                url(r'^login/$', 'profiles.viewslogin.loginView'),
                url(r'^logout/$', 'profiles.viewslogin.logoutView'),

                # explore/browse: most views, most faved, most recent, and staff picks
                #url(r'^library/browse/views/$','search.viewsexplore.browseViews,name='browse_views'),
                #url(r'^library/browse/faved/$','search.viewsexplore.browseFaved,name='browse_faves'),
                url(r'^library/browse/recent/$', 'uploads.viewsexplore.browseRecent', name='browse_recent'),
                url(r'^library/browse/staff/$','uploads.viewsexplore.browseStaffPicks',name='browse_staffpicks'),

                # user features
                url(r'^profile/my_dashboard/$', 'uploads.viewsdashboard.getDashboard', name='dashboard'),
                url(r'^profile/my_submissions/$', 'uploads.viewsuploadsmanager.uploadsManager', name='uploadsmanager'),
                    
                # submission of a scene or animation file
                url(r'^profile/upload/$', 'uploads.viewssubmission.createSubmission', name='upload'),
                #url(r'^profile/upload/delete/$', 'uploads.viewssubmissionn.MFBSubmission', name='upload-delete'),
                
                # revision of a submission, pk is of submission object
                url(r'^profile/submission/(?P<pkVid>\d+)/revise/$', 'uploads.viewsrevision.createRevision', name='revise'), 
                #display latest revision; pk is of Revision object
                url(r'^profile/revision/pk/(?P<revPk>\d+)/$', 'uploads.viewsrevision.getRevInfo', name='revinfo'),
                
                # specific submission object with latest revision object of a given member (end-user can be logged in or not)
                url(r'^submission/pk/(?P<subPk>\d+)/revpk/(?P<revPk>\d+)/$','uploads.viewsrevision.getSubInfo',name="subinfo" ),

)
