from dataclasses import make_dataclass
from enum import Enum
from itertools import chain

from django.db import models

from django_lookups.utils import classproperty


class LookupModel(models.Model):
    name = models.CharField(blank=False, null=False, max_length=32)

    class enum(Enum):
        """
        Subclass this to extend your members enum for more complicated lookup records.
        """

        @property
        def id(self):
            return self.value.id

        @property
        def pk(self):
            return self.id

        @property
        def model(self):
            return self.value.model_class(name=self.name, id=self.id)

        def __str__(self):
            return self.name

    @classproperty
    def members(cls):  # noqa
        """
        An enumeration of all of the data in the lookup table.
        The member elements are a dataclass with the same fields
        as the model records.
        """
        try:
            return cls._members
        except AttributeError:
            pass

        # each member has the same fields as a model instance, plus a reference
        # to the model class
        member_fields = chain(
            ("model_class",), (field.name for field in cls._meta.fields)
        )
        member_class = make_dataclass(
            f"{cls.__name__}MemberElement",
            member_fields,
            frozen=True,
        )
        cls._members = cls.enum(
            f"{cls.__name__}Members",
            {
                lookup.name: _member_class_from_model(cls, member_class, lookup)
                for lookup in cls.objects.all()
            },
        )
        return cls._members

    @classmethod
    def member_from_pk(cls, pk):
        model = cls.objects.get(pk=pk)
        return getattr(cls.members, model.name)

    class Meta:
        abstract = True


def _member_class_from_model(cls, member_class, model):
    instance_variables = {
        field.name: getattr(model, field.name) for field in cls._meta.fields
    }
    return member_class(model_class=model.__class__, **instance_variables)
