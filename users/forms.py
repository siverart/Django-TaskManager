from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import CustomUser




class RegisterForm(UserCreationForm):
	email = forms.EmailField(
							required=True,
						   help_text="กรุณาใส่อีเมลที่ใช้งานจริงเพื่อยืนยันตัวตน",
						   widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'})
						   )
	first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	
	last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	

	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ("username", "email", "first_name", "last_name")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
        # ทางลัด: วนลูปใส่ class 'form-control' ให้ทุกฟิลด์ในฟอร์ม (รวมถึง username/password)
		for field in self.fields.values():
			field.widget.attrs.update({'class': 'form-control'})

		