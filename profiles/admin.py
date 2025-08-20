from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Gender, Caste, Subcaste, SiblingInfo, Profile, Company, Review, BlogPost, Slider, Service, Client, About, Contact, SEO
from .widgets import HoroscopeWidget
from .forms import ProfileForm

# Title bar la kaatum peyar
admin.site.site_title = "Punagai Matrimony Admin"

# Top header la kaatum peyar
admin.site.site_header = "Punagai Matrimony Admin"

# Dashboard (home page) la kaatum peyar
admin.site.index_title = "Welcome to Punagai Admin Matrimony Dashboard"

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class SubcasteInline(admin.TabularInline):
    model = Subcaste
    extra = 1


@admin.register(Caste)
class CasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    inlines = [SubcasteInline]


@admin.register(Subcaste)
class SubcasteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'caste')
    list_filter = ('caste',)
    search_fields = ('name', 'caste__name')


class SiblingInfoInline(admin.TabularInline):
    model = SiblingInfo
    extra = 1
    fields = ('relationship', 'marital_status', 'count')
    verbose_name_plural = "Siblings Information"

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'rasi_1': forms.TextInput(attrs={'placeholder': 'Rasi 1'}),
            'rasi_2': forms.TextInput(attrs={'placeholder': 'Rasi 2'}),
            'rasi_3': forms.TextInput(attrs={'placeholder': 'Rasi 3'}),
            'rasi_4': forms.TextInput(attrs={'placeholder': 'Rasi 4'}),
            'rasi_5': forms.TextInput(attrs={'placeholder': 'Rasi 5'}),
            'rasi_empty1': forms.TextInput(attrs={'placeholder': 'empty 1'}),
            'rasi_empty2': forms.TextInput(attrs={'placeholder': 'empty 2'}),
            'rasi_6': forms.TextInput(attrs={'placeholder': 'Rasi 6'}),
            'rasi_7': forms.TextInput(attrs={'placeholder': 'Rasi 7'}),
            'rasi_empty3': forms.TextInput(attrs={'placeholder': 'empty 3'}),
            'rasi_empty4': forms.TextInput(attrs={'placeholder': 'empty 4'}),
            'rasi_8': forms.TextInput(attrs={'placeholder': 'Rasi 8'}),
            'rasi_9': forms.TextInput(attrs={'placeholder': 'Rasi 9'}),
            'rasi_10': forms.TextInput(attrs={'placeholder': 'Rasi 10'}),
            'rasi_11': forms.TextInput(attrs={'placeholder': 'Rasi 11'}),
            'rasi_12': forms.TextInput(attrs={'placeholder': 'Rasi 12'}),
            'amsam_1': forms.TextInput(attrs={'placeholder': 'Amsam 1'}),
            'amsam_2': forms.TextInput(attrs={'placeholder': 'Amsam 2'}),
            'amsam_3': forms.TextInput(attrs={'placeholder': 'Amsam 3'}),
            'amsam_4': forms.TextInput(attrs={'placeholder': 'Amsam 4'}),
            'amsam_5': forms.TextInput(attrs={'placeholder': 'Amsam 5'}),
            'amsam_empty1': forms.TextInput(attrs={'placeholder': 'empty 1'}),
            'amsam_empty2': forms.TextInput(attrs={'placeholder': 'empty 2'}),
            'amsam_6': forms.TextInput(attrs={'placeholder': 'Amsam 6'}),
            'amsam_7': forms.TextInput(attrs={'placeholder': 'Amsam 7'}),
            'amsam_empty3': forms.TextInput(attrs={'placeholder': 'empty 3'}),
            'amsam_empty4': forms.TextInput(attrs={'placeholder': 'empty 4'}),
            'amsam_8': forms.TextInput(attrs={'placeholder': 'Amsam 8'}),
            'amsam_9': forms.TextInput(attrs={'placeholder': 'Amsam 9'}),
            'amsam_10': forms.TextInput(attrs={'placeholder': 'Amsam 10'}),
            'amsam_11': forms.TextInput(attrs={'placeholder': 'Amsam 11'}),
            'amsam_12': forms.TextInput(attrs={'placeholder': 'Amsam 12'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter subcaste list dynamically
        if 'caste' in self.data:
            try:
                caste_id = int(self.data.get('caste'))
                self.fields['subcaste'].queryset = Subcaste.objects.filter(caste_id=caste_id)
            except (ValueError, TypeError):
                self.fields['subcaste'].queryset = Subcaste.objects.none()
        elif self.instance.pk and self.instance.caste:
            self.fields['subcaste'].queryset = Subcaste.objects.filter(caste=self.instance.caste)
        else:
            self.fields['subcaste'].queryset = Subcaste.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        # No need for special cleaning since we're using individual fields now
        return cleaned_data


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ('full_name', 'gender', 'age', 'caste', 'subcaste', 'approved', 'photo_preview')
    list_filter = ('approved', 'gender', 'caste', 'subcaste', 'marital_status')
    search_fields = (
        'full_name', 'city', 'state', 'occupation', 'education',
        'caste__name', 'subcaste__name', 'contact_number', 'email'
    )
    autocomplete_fields = ('gender', 'caste', 'subcaste')
    readonly_fields = ('age', 'photo_preview', 'photo2_preview', 'siblings_summary')
    inlines = [SiblingInfoInline]
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'full_name', 'gender', 'dob', 'birth_time', 'age',
                'caste', 'subcaste', 'language', 'mother_tongue'
            )
        }),
        ('Astrological Details', {
            'fields': (
                'gothram', 'star', 'rasi',
                'dasa_balance', 'dasa_years', 'dasa_months', 'dasa_days',
                ('rasi_1', 'rasi_2', 'rasi_3', 'rasi_4'),
                ('rasi_5', 'rasi_empty1', 'rasi_empty2','rasi_6'),
                ('rasi_7', 'rasi_empty3','rasi_empty4', 'rasi_8'),
                ('rasi_9', 'rasi_10', 'rasi_11', 'rasi_12'),
                ('amsam_1', 'amsam_2', 'amsam_3', 'amsam_4'),
                ('amsam_5', 'amsam_empty1', 'amsam_empty2','amsam_6'),
                ('amsam_7', 'amsam_empty3','amsam_empty4', 'amsam_8'),
                ('amsam_9', 'amsam_10', 'amsam_11', 'amsam_12'),
            )
        }),
        ('Physical Attributes', {
            'fields': (
                'height_cm', 'weight_kg', 'complexion', 'disability', 'diet'
            )
        }),
        ('Education & Career', {
            'fields': (
                'education', 'occupation', 'income', 'place_of_job'
            )
        }),
        ('Family Details', {
            'fields': (
                'father_alive', 'mother_alive', 'father_occupation', 'mother_occupation',
                'siblings_summary', 'native_place'
            )
        }),
        ('Location', {
            'fields': (
                'city', 'state', 'country', 'place_of_birth'
            )
        }),
        ('Personal Details', {
            'fields': (
                'marital_status', 'about'
            )
        }),
        ('Partner Expectations', {
            'fields': (
                'expected_qualification', 'expected_job', 'expected_income',
                'expected_caste', 'expected_subcaste', 'expected_diet',
                'expected_marital_status', 'other_expectations'
            )
        }),
        ('Photos', {
            'fields': (
                'photo', 'photo_preview', 'photo2', 'photo2_preview'
            )
        }),
        ('Contact Information', {
            'fields': (
                'contact_person', 'contact_number', 'alternate_contact', 'email'
            )
        }),
        ('System Fields', {
            'fields': (
                'approved', 'slug'
            )
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.photo.url)
        return "-"
    photo_preview.short_description = 'Photo Preview'

    def photo2_preview(self, obj):
        if obj.photo2:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.photo2.url)
        return "-"
    photo2_preview.short_description = 'Second Photo Preview'

    def siblings_summary(self, obj):
        if obj.pk:
            counts = obj.get_sibling_counts()
            summary = []
            for rel, status_counts in counts.items():
                for status, count in status_counts.items():
                    if count > 0:
                        rel_display = rel.replace('_', ' ').title()
                        status_display = status.title()
                        summary.append(f"{count} {rel_display} ({status_display})")
            return format_html("<br>".join(summary)) if summary else "No siblings"
        return "Save profile first to add siblings"
    siblings_summary.short_description = 'Siblings Summary'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:  # editing an existing object
            return readonly_fields + ('created_at', 'updated_at')
        return readonly_fields


@admin.register(SiblingInfo)
class SiblingInfoAdmin(admin.ModelAdmin):
    list_display = ('profile', 'get_relationship_display', 'get_marital_status_display', 'count')
    list_filter = ('relationship', 'marital_status')
    search_fields = ('profile__full_name',)
    autocomplete_fields = ('profile',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone1')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone1', 'phone2', 'address')
        }),
        ('Social Media', {
            'fields': ('website', 'whatsapp', 'instagram'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("title", "short_desc")

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("email", "phone")

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("address", "email", "phone")

@admin.register(SEO)
class SEOAdmin(admin.ModelAdmin):
    list_display = ("page_name", "title", "updated_at")
    search_fields = ("page_name", "title", "keywords")