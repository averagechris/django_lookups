# django_lookups: Lookup Models for Django Applications

django_lookups provides a LookupModel that many of us have written some variation 100's of times. Most of the applications we write have lookup tables (or should!) and we have boilerplate everywhere to manage constants. The aim of this library is to make working with lookup data in django easier.

You might have a constants repo / package / library that you share between your apps or services. Most of the time, instead of constants, those values really belong in lookup tables. Things like status int fields. If you have a django model with a field like `status = models.PositiveIntegerField` this library is probably for you!


A trivial example showing how you might interact with an Order Status.
```python
class OrderStatusTypes(django_lookups.LookupModel):
    class Meta:
        app_label = "my_app"
        db_tabel = "my_table"

class Order(models.Model):
    status = models.ForeignKey(OrderStatusTypes)
    address = models.ForeignKey(...)
    created = models.TimestampField()
    changed = models.TimestampField()

    @classmethod
    def new_order(cls):
        return cls.objects.create(
            status=OrderStatusTypes.members.INITIATED.model,
            ...
        )
```


Once you add this library as a dependency, and have created your first lookup model, you'll need to run a [data migration](https://docs.djangoproject.com/en/3.1/topics/migrations/#data-migrations) to add the lookup values to your table, or add data to your lookup tables manually. Once the data is there, your code can work with this data by name. No more need to keep constants libraries in sync when you add a new type/status etc!


This library is on pypi so you can run `pip install django_lookups` to get started or add it with the package manager of your choice.
