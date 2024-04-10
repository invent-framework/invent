from toga import Box


class Row(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style.direction = "row"


class Column(Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.style.direction = "column"
