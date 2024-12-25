from django import forms
from .models import Product, HashTag

class ProductForm(forms.ModelForm):
    hashtags_str = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'hashtags_str'] 

    def clean_hashtags(self):
        hashtags = self.cleaned_data['hashtags']
        for hashtag in hashtags:
            if not hashtag.isalpha():
                raise forms.ValidationError('해시태그는 알파벳만 가능합니다!')
        return hashtags

    def save(self, commit=True):
        product = super().save(commit=False)
        
        if self.user:
            product.user = self.user
            
        if commit:
            product.save()
            
            hashtags_input = self.cleaned_data.get('hashtags_str', '')
            hashtag_list = [h for h in hashtags_input.replace(',', ' ').split() if h]
            new_hashtags = []
            for ht in hashtag_list:
                ht_obj, created = HashTag.objects.get_or_create(name=ht)
                new_hashtags.append(ht_obj)
        

        # 다대다 관계 설정
        product.hashtags.set(new_hashtags)

        if not commit:
            product.save()
            

        return product
