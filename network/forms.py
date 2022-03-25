from django import forms


class NewPostForm(forms.Form):
    content = forms.CharField(
        max_length=256,
        widget=forms.Textarea(
            attrs={
                "class": "textarea p-4",
                "placeholder": "What's up?",
            }
        ),
    )
