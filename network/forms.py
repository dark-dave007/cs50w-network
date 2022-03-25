from django import forms


class NewPostForm(forms.Form):
    content = forms.CharField(
        max_length=256,
        widget=forms.Textarea(
            attrs={
                "class": "textarea",
                "placeholder": "What's up?",
            }
        ),
    )
