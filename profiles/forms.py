from django import forms
from .models import Profile, Caste, Subcaste, Gender, Company, ContactMessage
import json
# class FilterForm(forms.Form):
    # gender = forms.ModelChoiceField(queryset=Gender.objects.all(), required=False, empty_label="Any")
    # caste = forms.ModelChoiceField(queryset=Caste.objects.all(), required=False, empty_label="Any")
    # subcaste = forms.ModelChoiceField(queryset=Subcaste.objects.none(), required=False, empty_label="Any")
    # age_min = forms.IntegerField(required=False, min_value=18)
    # age_max = forms.IntegerField(required=False, min_value=18)

    # def __init__(self, *args, **kwargs):
    #     caste_id = None
    #     if 'data' in kwargs and kwargs['data'].get('caste'):
    #         caste_id = kwargs['data'].get('caste')
    #     super().__init__(*args, **kwargs)
    #     if caste_id:
    #         self.fields['subcaste'].queryset = Subcaste.objects.filter(caste_id=caste_id)
    #     else:
    #         # keep subcaste empty until caste is selected
    #         self.fields['subcaste'].queryset = Subcaste.objects.none()


class ProfileForm(forms.ModelForm):
    caste = forms.ModelChoiceField(queryset=Caste.objects.all())
    subcaste = forms.ModelChoiceField(queryset=Subcaste.objects.all(), required=False)

    class Meta:
        model = Profile
        fields = [
            'full_name', 'gender', 'caste', 'subcaste', 'dob', 'age',
            'language', 'education', 'occupation', 'income',
            'height_cm', 'weight_kg', 'marital_status',
            'city', 'state', 'country', 'about', 'photo',
            'approved', 'slug'
        ]

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class FilterForm(forms.Form):
    gender = forms.ModelChoiceField(
        queryset=Gender.objects.all(), required=False, empty_label="Any",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    caste = forms.ModelChoiceField(
        queryset=Caste.objects.all(), required=False, empty_label="Any",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    subcaste = forms.ModelChoiceField(
        queryset=Subcaste.objects.none(), required=False, empty_label="Any",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    age_min = forms.IntegerField(
        required=False, min_value=18,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min Age"})
    )
    age_max = forms.IntegerField(
        required=False, min_value=18,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max Age"})
    )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # caste_id எடுக்க form data → self.data (GET or POST)
        caste_id = self.data.get("caste") or self.initial.get("caste")

        if caste_id:
            try:
                self.fields["subcaste"].queryset = Subcaste.objects.filter(caste_id=caste_id)
            except (ValueError, TypeError):
                self.fields["subcaste"].queryset = Subcaste.objects.none()
        else:
            self.fields["subcaste"].queryset = Subcaste.objects.none()

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Phone"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Your Message"}),
        }


class HoroscopeWidget(forms.Widget):
    template_name = "widgets/horoscope_widget.html"

    def format_value(self, value):
        if not value:
            return ["" for _ in range(12)]
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return ["" for _ in range(12)]
        return value

    def value_from_datadict(self, data, files, name):
        return [data.get(f"{name}_{i}", "") for i in range(12)]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Combine rasi_cells inputs into rasi_1..12
        rasi_inputs = [self.cleaned_data.get(f"rasi_{i+1}") for i in range(12)]
        for i, val in enumerate(rasi_inputs):
            setattr(instance, f"rasi_{i+1}", val)

        # Combine amsam_cells inputs into amsam_1..12
        amsam_inputs = [self.cleaned_data.get(f"amsam_{i+1}") for i in range(12)]
        for i, val in enumerate(amsam_inputs):
            setattr(instance, f"amsam_{i+1}", val)

        if commit:
            instance.save()
        return instance

