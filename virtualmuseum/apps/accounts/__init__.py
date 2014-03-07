#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.management import create_superuser
from django.db.models import signals
from django.contrib.auth import models as auth_models
from django.conf import settings

signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_models,
    dispatch_uid='django.contrib.auth.management.create_superuser'
)

def create_admin(app, created_models, verbosity, **kwargs):
    
    user = 'admin'
    email = 'admin@admin.com'
    password = 'admin'
    
    try:
        auth_models.User.objects.get(username='admin')
    except auth_models.User.DoesNotExist:
        print ''
        print '-' * 80
        print 'Creating admin user with login: %s and password: %s' % (user, password)
        print '-' * 80
        print ''
        assert auth_models.User.objects.create_superuser(user, email, password)


signals.post_syncdb.connect(
    create_admin,
    sender=auth_models,
    dispatch_uid='apps.auth.models.create_admin'
)
