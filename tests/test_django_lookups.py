from django.db import models
import pytest

from django_lookups.models import LookupModel


class StatusTypes(LookupModel):
    class Meta:
        db_table = "test_status_types"
        app_label = "default"


class ExtendedWithNewFields(LookupModel):
    description = models.CharField(blank=False, null=False, max_length=64)

    class enum(LookupModel.enum):
        @property
        def description(self):
            return self.value.description

    class Meta:
        db_table = "test_complicated_types"
        app_label = "default"


class MyModel(models.Model):
    status = models.ForeignKey(StatusTypes, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "test_my_model"
        app_label = "default"


@pytest.fixture(autouse=True)
def create_tables_and_reset__members(create_tables_from_models):
    all_models = [StatusTypes, ExtendedWithNewFields, MyModel]
    create_tables_from_models(*all_models)

    for model in all_models:
        try:
            del model._members
        except AttributeError:
            pass


def test_lookup_members(db):
    StatusTypes(name="INITIATED").save()
    assert StatusTypes.members.INITIATED.name == "INITIATED"
    assert StatusTypes.members.INITIATED.id == 1
    assert StatusTypes.members.INITIATED.pk == 1


def test_extended_with_new_fields(db):
    ExtendedWithNewFields(name="NEW", description="BRAND_NEW").save()
    assert ExtendedWithNewFields.members.NEW.name == "NEW"
    assert ExtendedWithNewFields.members.NEW.description == "BRAND_NEW"
    assert ExtendedWithNewFields.members.NEW.id == 1
    assert ExtendedWithNewFields.members.NEW.pk == 1


def test_member_model_property(db):
    StatusTypes(name="INITIATED").save()
    MyModel(status=StatusTypes.members.INITIATED.model).save()
    assert StatusTypes.members.INITIATED is StatusTypes.member_from_pk(
        MyModel.objects.first().status.pk
    )


def test_member_from_pk(db):
    with pytest.raises(StatusTypes.DoesNotExist):
        StatusTypes.member_from_pk(1)

    StatusTypes(name="ONE").save()
    assert "ONE" == StatusTypes.member_from_pk(1).name
    assert StatusTypes.members.ONE


def test_invalid_member_raises_AttributeError(db):
    with pytest.raises(AttributeError):
        StatusTypes.members.DEFINITELY_DOES_NOT_EXIST
