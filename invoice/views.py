######################################## By - Adebisi Ayomide ######################################

from django.shortcuts import render
from xero import Xero
from xero.auth import OAuth2Credentials
from xero.constants import XeroScopes
from django.http import HttpResponseRedirect,HttpResponse
from django.core.cache import cache
from django.views import View
from .forms import  InvoiceForm

# Create your views here.

client_id = '60C8B19E86FC4791A5B83858C00A7AE4'
client_secret = 'DcD0qhLRN4ZJI55251Gz-VYCoKZTi6sYWVK8qyXJ7O6LdHgp'
callback_uri = 'https://localhost:8080/activate/'


class AuthorizeView(View):
    greeting = "Good Day"

    def get(self, request):
      return render(request,'index.html', context={})

    def post(self, request):
      credentials = OAuth2Credentials(
        client_id, client_secret, callback_uri=callback_uri,
        scope=[XeroScopes.OFFLINE_ACCESS, XeroScopes.ACCOUNTING_CONTACTS,
              XeroScopes.ACCOUNTING_TRANSACTIONS]
      )
      authorization_url = credentials.generate_url()
      cache.set('xero_creds', credentials.state)
      return HttpResponseRedirect(authorization_url)
class CreateInvoiceView(View):

  author = '__alsaheem__'
  set_cred = ''
  def get(self, request):
    form = InvoiceForm()
    cred_state = cache.get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    auth_secret = request.get_raw_uri()
    credentials.verify(auth_secret)
    credentials.set_default_tenant()
    cred_state = credentials.state
    credentials = OAuth2Credentials(**cred_state)
    cache.set('xero_creds', credentials.state)
    if credentials.expired():
      credentials.refresh()
      cache.set('xero_creds', credentials.state)

    return render(request,'activate.html', context={'form':form})

  def post(self,request):
    form = InvoiceForm(request.POST)
    cred_state = cache.get('xero_creds')
    credentials = OAuth2Credentials(**cred_state)
    xero = Xero(credentials)
    if form.is_valid():
      Type = form.cleaned_data['Type']
      ContactID = form.cleaned_data['ContactID']
      DateString = form.cleaned_data['DateString']
      DueDateString = form.cleaned_data['DueDateString']
      LineAmountTypes = form.cleaned_data['LineAmountTypes']
      Description = form.cleaned_data['Description']
      Quantity = form.cleaned_data['Quantity']
      UnitAmount = form.cleaned_data['UnitAmount']
      AccountCode = form.cleaned_data['AccountCode']
      DiscountRate = form.cleaned_data['DiscountRate']
      data = {
        "Type": Type,
        "Contact": {
          "ContactID": str(ContactID)
        },
        "DateString": str(DateString),
        "DueDateString": str(DueDateString),
        "LineAmountTypes": str(LineAmountTypes),
        "LineItems": [
          {
            "Description": str(Description),
            "Quantity": str(Quantity),
            "UnitAmount": str(UnitAmount),
            "AccountCode": str(AccountCode),
            "DiscountRate": str(DiscountRate)
          }
        ],
         "Status": "AUTHORISED"
      }
      # process the data in form.cleaned_data as required
      xero.invoices.put(data)
      return HttpResponse('valid Details sent')
    else:
      return HttpResponse('Invalid Details')
