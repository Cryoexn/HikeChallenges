from bootstrap_datepicker_plus import DatePickerInput
from django import forms

class AchievementForm(forms.Form):
	is_done = forms.BooleanField(required=False)
	date_done = forms.DateField(widget=DatePickerInput(format="%m/%d/%Y"))
