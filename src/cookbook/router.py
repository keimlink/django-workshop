class NewsRouter(object):
    """A router to control all database operations on models in the news application.
    """
    def db_for_read(self, model, **hints):
        "Point all operations on the news app models to newsdb."
        if model._meta.app_label == 'news':
            return 'newsdb'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on the news app models to newsdb."
        if model._meta.app_label == 'news':
            return 'newsdb'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow no relation if a model in news app is involved."
        if obj1._meta.app_label == 'news' or obj2._meta.app_label == 'news':
            return False
        return None

    def allow_syncdb(self, db, model):
        "Make sure the news app only appears on the newsdb."
        allowed = ['south']
        if model._meta.app_label in allowed:
            return True
        elif db == 'newsdb':
            return model._meta.app_label == 'news'
        elif model._meta.app_label == 'news':
            return False
        return None
