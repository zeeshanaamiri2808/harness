class TodoApp:
    def __init__(self):
        self.items = []

    def add_item(self, text):
        if not text or not text.strip():
            raise ValueError("Item text cannot be empty")
        item = {"id": len(self.items) + 1, "text": text.strip(), "done": False}
        self.items.append(item)
        return item

    def get_items(self):
        return self.items

    def complete_item(self, item_id):
        for item in self.items:
            if item["id"] == item_id:
                item["done"] = True
                return item
        raise ValueError(f"Item {item_id} not found")

    def delete_item(self, item_id):
        for i, item in enumerate(self.items):
            if item["id"] == item_id:
                return self.items.pop(i)
        raise ValueError(f"Item {item_id} not found")

    def get_pending(self):
        return [item for item in self.items if not item["done"]]

    def get_completed(self):
        return [item for item in self.items if item["done"]]