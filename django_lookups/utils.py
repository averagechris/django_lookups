class classproperty(property):
    def __get__(self, *args, **kwargs):
        return classmethod(self.fget).__get__(*args, **kwargs)()
