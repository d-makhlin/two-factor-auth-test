import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"
