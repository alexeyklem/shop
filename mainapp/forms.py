from django import forms
from django.contrib.auth.models import User

from .models import Order

class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment'
        )

class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не найден в системе')#------------ выдает ошибку
        user = User.objects.filter(username=username).first()#----- проверка правильно ли ввел пароль
        if user:
            if not user.check_password(password): #------- проверяем соответствует ли введенный пароль найденному юзеру
                raise forms.ValidationError(f'Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
