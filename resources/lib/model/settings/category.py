class Category(object):
    def __init__(self, cat_id, cat_label, priority):
        self.cat_id = cat_id
        self.cat_label = cat_label
        self.priority = priority
        self.settings = {}
