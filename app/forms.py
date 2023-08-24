from django import forms

from hcaptcha_field import hCaptchaField
  
class CaptchaForm(forms.Form):
    captcha = hCaptchaField(label=False)