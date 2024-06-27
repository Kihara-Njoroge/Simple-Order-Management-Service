import factory
from django.db.models.signals import post_save
from faker import Factory as FakeFactory

from app.order_service.settings.base import AUTH_USER_MODEL

faker = FakeFactory.create()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    username = factory.Faker("user_name")
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: "password")
    is_active = True
    is_staff = False

    class Meta:
        model = AUTH_USER_MODEL

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        password = kwargs.pop("password", "password")  # Extract password
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, password=password, **kwargs)
        else:
            return manager.create_user(*args, password=password, **kwargs)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """
        Save again the instance if creating and at least one hook ran.
        """
        if create and results:
            instance.save()
