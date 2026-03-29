class DisplayMixin:
    def get_display_fields(self):
        return []

    def __str__(self):
        parts = []

        for field in self.get_display_fields():
            if callable(field):
                parts.append(str(field(self)))
            else:
                value = getattr(self, field, None)
                parts.append(str(value))

        return " - ".join(parts)
