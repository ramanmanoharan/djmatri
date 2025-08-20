from django import forms
import json

class HoroscopeWidget(forms.Widget):
    template_name = "widgets/horoscope_widget.html"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format_value(self, value):
        if not value:
            return ["" for _ in range(12)]
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return ["" for _ in range(12)]
        return value

    def value_from_datadict(self, data, files, name):
        return [data.get(f"{name}_{i}", "") for i in range(12)]
