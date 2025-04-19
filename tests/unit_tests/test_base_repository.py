from pytest import raises
from src.infrastructure.database.repository import EntityRepository


def test_create_repository_without_entity_attribute_fail():
    with raises(AttributeError):

        class TestRepository(EntityRepository):
            pass
