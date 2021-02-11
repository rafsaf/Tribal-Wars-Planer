class Mode:
    def __init__(self, request_GET_mode: str):
        VALID = [
            "menu",
            "time",
            "fake",
            "add_and_remove",
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

    @property
    def is_add_and_remove(self):
        return self.mode == "add_and_remove"

    def __str__(self):
        return self.mode

class TargetMode:
    def __init__(self, request_GET_mode: str):
        VALID = [
            "real",
            "fake",
            "ruin",
        ]

        if request_GET_mode is None:
            self.mode = "real"
        else:
            if request_GET_mode in VALID:
                self.mode = request_GET_mode
            else:
                self.mode = "real"
    @property
    def is_real(self):
        return self.mode == "real"

    @property
    def is_fake(self):
        return self.mode == "fake"

    @property
    def is_ruin(self):
        return self.mode == "ruin"

    @property
    def fake(self):
        if self.is_fake:
            return True
        return False
    
    @property
    def ruin(self):
        if self.is_ruin:
            return True
        return False