from django.forms import CheckboxSelectMultiple


class ArraySelectMultiple(CheckboxSelectMultiple):
    def value_omitted_from_data(self, data, files, name):
        return False
