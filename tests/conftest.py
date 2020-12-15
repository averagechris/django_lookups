import pytest
from django.db import connection


@pytest.fixture
def create_tables_from_models(django_db_blocker, django_db_use_migrations):
    created_models = []

    def model_adder(*models):
        if not django_db_use_migrations:
            return

        with django_db_blocker.unblock(), connection.schema_editor(
            atomic=True
        ) as schema_editor:
            for model in models:
                schema_editor.create_model(model)
                created_models.append(model)

    yield model_adder

    if created_models:
        with django_db_blocker.unblock(), connection.schema_editor(
            atomic=True
        ) as schema_editor:
            for model in created_models:
                schema_editor.delete_model(model)
