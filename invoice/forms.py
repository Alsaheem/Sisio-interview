from django import forms

class InvoiceForm(forms.Form):
  Type = forms.CharField(max_length=100)
  ContactID = forms.CharField(max_length=100,initial='39cd38d64add46ab85225f33918becc1')
  DateString = forms.DateField()
  DueDateString = forms.DateField()
  Type = forms.CharField(max_length=100)
  LineAmountTypes = forms.CharField(max_length=100)
  Description = forms.CharField(widget=forms.Textarea)
  Quantity = forms.CharField(max_length=100)
  UnitAmount = forms.IntegerField()
  AccountCode = forms.IntegerField()
  DiscountRate = forms.IntegerField()

