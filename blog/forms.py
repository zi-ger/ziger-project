from .models import UserPost
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset

class UserPostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('text',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ('text', 'parent')
    
class HelpForm(forms.Form):
    sender = forms.EmailField(required=True, label='Email')
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, label='Message')


    def __init__(self, *args, **kwargs):
        super(HelpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('sender', css_class='form-group col-md-6'),
                Column('subject', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'message'
        )
        self.helper.add_input(Submit('submit', 'Send'))