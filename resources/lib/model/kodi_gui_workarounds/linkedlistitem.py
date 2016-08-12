class LinkedListItem(object):
    def __init__(self, item, previous_item=None, next_item=None):
        self.item = item
        self.previous_item = previous_item
        self.next_item = next_item

    def __get__(self, instance, owner):
        return self.item

    def __getattr__(self, name):
        return getattr(self.item, name)

    def has_next(self):
        return self.next_item is not None

    def has_previous(self):
        return self.previous_item is not None

    def get_next(self):
        return self.next_item

    def get_previous(self):
        return self.previous_item

    def set_next(self, next_item):
        if next_item != self.next_item:
            self.next_item = next_item
            next_item.set_previous(self)

    def set_previous(self, previous_item):
        if previous_item != self.previous_item:
            self.previous_item = previous_item
            previous_item.set_next(self)

    def get_x_previous(self, x):
        x = int(x)
        previous = self
        while x < 0:
            previous = previous.get_previous()
            x += 1
        return previous

    def get_x_next(self, x):
        x = int(x)
        next_item = self
        while x > 0:
            next_item = next_item.get_next()
            x -= 1
        return next_item
