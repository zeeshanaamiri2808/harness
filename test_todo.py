import pytest
from todo import TodoApp


@pytest.fixture
def app():
    return TodoApp()


def test_add_item_preserves_case(app):
    item = app.add_item("Buy groceries")
    assert item["text"] == "Buy groceries", (
        f"Expected 'Buy groceries' but got '{item['text']}' — "
        "item text must not be modified"
    )


def test_add_item_returns_correct_id(app):
    item1 = app.add_item("First task")
    item2 = app.add_item("Second task")
    assert item1["id"] == 1
    assert item2["id"] == 2


def test_add_item_starts_not_done(app):
    item = app.add_item("Write report")
    assert item["done"] is False


def test_complete_item(app):
    app.add_item("Send email")
    result = app.complete_item(1)
    assert result["done"] is True
    assert app.get_completed()[0]["id"] == 1


def test_delete_item(app):
    app.add_item("Clean desk")
    app.delete_item(1)
    assert len(app.get_items()) == 0


def test_empty_item_raises(app):
    with pytest.raises(ValueError):
        app.add_item("")


def test_pending_vs_completed_split(app):
    app.add_item("Task A")
    app.add_item("Task B")
    app.complete_item(1)
    assert len(app.get_pending()) == 1
    assert len(app.get_completed()) == 1
