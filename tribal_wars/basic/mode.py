class Mode:
    def __init__(self, request_GET_mode: str):
        VALID = [
            "menu",
            "time",
            "fake",
        ]

        if request_GET_mode is None:
            self.mode = "menu"
        else:
            if request_GET_mode in VALID:
                self.mode = request_GET_mode
            else:
                self.mode = "menu"

    @property
    def is_menu(self):
        return self.mode == "menu"

    @property
    def is_time(self):
        return self.mode == "time"

    @property
    def is_fake(self):
        return self.mode == "fake"

    def __str__(self):
        return self.mode
