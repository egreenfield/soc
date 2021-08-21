from typing import ClassVar


class ID:
    lastID:ClassVar[int] = 0

    @classmethod
    def allocate(self):
        self.lastID += 1
        return self.lastID

