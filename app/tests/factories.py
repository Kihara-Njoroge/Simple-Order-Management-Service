import factory
from django.db.models.signals import post_save
from faker import Factory as FakeFactory

from app.order_service.settings.base import AUTH_USER_MODEL

faker = FakeFactory.create()


# user factory
@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    username = factory.LazyAttribute(lambda x: faker.first_name())
    phone_number = factory.LazyAttribute(lambda x: faker.phone_number())
    email = factory.LazyAttribute(lambda x: faker.email())
    password = "Password@1"
    is_active = True
    is_staff = False

    class Meta:
        model = AUTH_USER_MODEL

    # controls whether to create a normal user or a super user
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)
