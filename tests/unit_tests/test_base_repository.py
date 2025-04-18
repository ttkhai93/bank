from pytest import raises
from src.domain.repositories.base import BaseRepository


def test_create_repository_without_entity_attribute_fail():
    with raises(AttributeError):

        class TestRepository(BaseRepository):
            pass
