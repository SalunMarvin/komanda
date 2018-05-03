from django import forms

class AddTicketForm(forms.Form):
    ticket_name = forms.CharField(label='Nome', max_length=100, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    ticket_number = forms.IntegerField(
        label='Número', required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
