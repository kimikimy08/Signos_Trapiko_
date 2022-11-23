import datetime
from django import forms
from django.conf import settings
from .models import Sent
from ckeditor.widgets import CKEditorWidget

class SentMessage(forms.ModelForm):
    message = forms.CharField(widget = CKEditorWidget())
    
    class Meta:
        model = Sent
        fields = [ 'to_email', 'subject',  'message']

    def __init__(self, *args, **kwargs):
        super(SentMessage, self).__init__(*args, **kwargs)
        self.fields['to_email'].widget.attrs['class'] = 'form-control mb-2'
        self.fields['subject'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        
