class CookbookRouter(object):
    """A router to control all database operations on models in the cookbook site.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'news':
            return 'newsdb'
        if model._meta.app_label == 'addressbook':
            return 'addressdb'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'news':
            return 'newsdb'
        if model._meta.app_label == 'addressbook':
            return 'addressdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'news' or obj2._meta.app_label == 'news':
            return False
        if obj1._meta.app_label == 'addressbook' or obj2._meta.app_label == 'addressbook':
            return False
        return None

    def allow_syncdb(self, db, model):
        allowed = ['south']
        if model._meta.app_label in allowed:
            return True
        elif db == 'newsdb':
            return model._meta.app_label == 'news'
        elif model._meta.app_label == 'news':
            return False
        return None
