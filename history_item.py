class HistoryItem:
    def __init__(self, from_status, to_status, author, created):
        self.from_status = from_status
        self.to_status = to_status
        self.author = author
        self.created = created