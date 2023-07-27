from django import forms
from .models import Certificate
from django.contrib.auth.models import User
from django.forms import DateField,SelectDateWidget


class CertificateForm(forms.ModelForm):
    #issued_at = DateField(widget=forms.SelectDateWidget())
    


    class Meta:
        model = Certificate
        fields = ("header","name","content","certified_by","issued_at",)
        #fields = '__all__'
        widgets ={
                'header':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'Certificate Name or Exam Name. **Optional max word:15'}),
                'name':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'Put Your Name here.'}),
                'content':forms.Textarea(attrs={'class':'form-control  w-50 ', 'placeholder':'**Optional. max word:320'}),      
                'issued_at':SelectDateWidget(attrs={'class':' m-1 form-select form-control  w-25 '}),
                'certified_by':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'"Authority" , "Certifier", "Institute" etc. '}),
            }


from django import forms


class TokenVerificationForm(forms.Form):
    token = forms.CharField(label='Certificate Token', max_length=1000,widget=forms.Textarea(attrs={'class':'form-control w-50 ','id':'floatingTextarea', 
    'style':'height:70px;','placeholder':'Paste Token or Certificate Code Here.'}))

    
class UpdateCertificateForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = ['name', 'header', 'issued_at', 'certified_by']
        widgets ={
                'header':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'Certificate Name or Exam Name. **Optional max word:15'}),
                'name':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'Put Your Name here.'}),
                'issued_at':SelectDateWidget(attrs={'class':' m-1 form-select form-control  w-25 '}),
                'certified_by':forms.TextInput(attrs={'class':'form-control  w-50 ', 'placeholder':'"Authority" , "Certifier", "Institute" etc. '}),
            }