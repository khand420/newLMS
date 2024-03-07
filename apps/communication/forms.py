# from django import forms
# from .models import Product
# #DataFlair

# class ProductCreate(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
#             visible.field.widget.attrs['placeholder'] = visible.field.label
#     class Meta:
#         model = Product
#         exclude = ('slug','created_at')
#         #fields = '__all__'


from django import forms
from .models import Communication

class CommunicationCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label
    
    class Meta:
        model = Communication
        exclude = ('created_at', 'client_id', 'updated_at', 'created_by','updated_by')
