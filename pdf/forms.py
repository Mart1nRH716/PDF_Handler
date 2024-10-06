from django import forms

from pdf.models import *


class PDFExtractForm(forms.ModelForm):
    class Meta:
        model = PDFFile
        fields = ['file', 'pages_to_extract']
        widgets = {
            'pages_to_extract': forms.TextInput(attrs={'placeholder': 'Ej: 1,2,3-5'}),
        }

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label="Seleccionar PDF")