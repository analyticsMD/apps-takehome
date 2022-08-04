import factory
import faker

from parts_api.models import Part


class TestParts(factory.DjangoModelFactory):
    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    sku = factory.Faker("ean")
    description = faker.Faker().text(max_nb_chars=1023)
    weight_ounces = factory.Faker("pyint", max_value=100)
    is_active = True

    class Meta:
        model = Part
