from pytest import raises
from src.infrastructure import EntityRepository


def test_create_child_entity_repository_without_entity_attribute_fail():
    with raises(AttributeError) as exc:

        class TestRepository(EntityRepository):
            pass

    assert str(exc.value) == "Class 'TestRepository' must define 'entity' class attribute"
