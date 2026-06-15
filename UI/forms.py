from django import forms
from django.core.validators import FileExtensionValidator

class FormUploadHwork(forms.Form):
    """ Formulario para subir tarea"""
    # code_homework = forms.CharField(widget=forms.TimeInput(attrs={"class":"code-homework", "placeholder":"Codigo de tarea", "id":"code-tarea"}))
    file_homework = forms.FileField(validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])
        ],widget=forms.FileInput(attrs={"class":"file-homework", "id":"file", 'accept': '.pdf, .doc, .docx, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document'}))

    # class Meta:
