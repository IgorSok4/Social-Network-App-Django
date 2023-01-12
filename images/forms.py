from urllib import request
from django import forms
from .models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(f'Provided URL address do not contain validate image format (it accepts only {valid_extensions} formats)')
        return url
    
    def save(self, force_insert=False,
                   force_update=False,
                   commit=True):
        image = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = '{}.{}'.format(slugify(image.title),
                                    image_url.rsplit('.', 1)[1].lower())
        
        #pobranie pliku obrazu z podanego adresu URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image