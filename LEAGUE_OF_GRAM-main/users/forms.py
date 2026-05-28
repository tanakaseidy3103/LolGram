from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'ユーザー名を入力してください'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'メールアドレスを入力してください'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワードを入力してください'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'パスワードを再入力してください'
        })
        
        self.error_messages = {
            'password_mismatch': 'パスワードが一致しません',
        }
        
        self.fields['username'].error_messages = {
            'required': 'ユーザー名を入力してください',
            'unique': 'このユーザー名は既に使用されています'
        }
        self.fields['email'].error_messages = {
            'required': 'メールアドレスを入力してください',
            'invalid': 'メールアドレスの形式が正しくありません'
        }
        self.fields['password1'].error_messages = {
            'required': 'パスワードを入力してください'
        }
        self.fields['password2'].error_messages = {
            'required': 'パスワードを再入力してください'
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError('ユーザー名は3文字以上である必要があります')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email:
            raise ValidationError('メールアドレスには@が必要です')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and len(password1) < 6:
            raise ValidationError('パスワードは6文字以上である必要があります')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('パスワードが一致しません')
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ユーザー名'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'パスワード'
    }))
    remember_me = forms.BooleanField(required=False)
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.error_messages = {
            'invalid_login': 'ユーザー名またはパスワードが正しくありません。',
            'inactive': 'このアカウントは無効です。',
        }

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }