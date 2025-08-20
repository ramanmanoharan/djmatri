from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from datetime import date

class Gender(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    class Meta:
        verbose_name_plural = "Genders"
    
    def __str__(self): 
        return self.name

class Caste(models.Model):
    name = models.CharField(max_length=120, unique=True)
    
    def __str__(self): 
        return self.name

class Subcaste(models.Model):
    caste = models.ForeignKey(Caste, related_name='subcastes', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    
    class Meta:
        unique_together = ('caste','name')
        ordering = ['name']
    
    def __str__(self): 
        return f"{self.caste} - {self.name}"

class SiblingInfo(models.Model):
    profile = models.ForeignKey('Profile', related_name='siblings', on_delete=models.CASCADE)
    RELATIONSHIP_CHOICES = [
        ('elder_brother', 'Elder Brother'),
        ('younger_brother', 'Younger Brother'),
        ('elder_sister', 'Elder Sister'),
        ('younger_sister', 'Younger Sister'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
    ]
    
    relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.get_relationship_display()} ({self.get_marital_status_display()}) - {self.count}"


class Profile(models.Model):
    exclude = ('created_at', 'updated_at', 'slug')  # exclude non-editable/system fields
    # Basic Information
    full_name = models.CharField(max_length=150)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
    caste = models.ForeignKey(Caste, on_delete=models.PROTECT, null=True, blank=True)
    subcaste = models.ForeignKey(Subcaste, on_delete=models.PROTECT, null=True, blank=True)
    
    # Birth Details
    dob = models.DateField(null=True, blank=True)
    birth_time = models.TimeField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    # Astrological Details
    gothram = models.CharField(max_length=100, blank=True)
    star = models.CharField(max_length=100, blank=True)
    rasi = models.CharField(max_length=100, blank=True)
    dasa_balance = models.CharField(max_length=100, blank=True)
    dasa_years = models.PositiveIntegerField(null=True, blank=True)
    dasa_months = models.PositiveIntegerField(null=True, blank=True)
    dasa_days = models.PositiveIntegerField(null=True, blank=True)
    
    # Rasi Box fields (12 cells)
    rasi_1 = models.CharField(max_length=100, blank=True)
    rasi_2 = models.CharField(max_length=100, blank=True)
    rasi_3 = models.CharField(max_length=100, blank=True)
    rasi_4 = models.CharField(max_length=100, blank=True)
    rasi_5 = models.CharField(max_length=100, blank=True)
    rasi_empty1 = models.CharField(max_length=100, blank=True)
    rasi_empty2 = models.CharField(max_length=100, blank=True)
    rasi_6 = models.CharField(max_length=100, blank=True)
    rasi_7 = models.CharField(max_length=100, blank=True)
    rasi_empty3 = models.CharField(max_length=100, blank=True)
    rasi_empty4 = models.CharField(max_length=100, blank=True)
    rasi_8 = models.CharField(max_length=100, blank=True)
    rasi_9 = models.CharField(max_length=100, blank=True)
    rasi_10 = models.CharField(max_length=100, blank=True)
    rasi_11 = models.CharField(max_length=100, blank=True)
    rasi_12 = models.CharField(max_length=100, blank=True)
    
    # Amsam Box fields (12 cells)
    amsam_1 = models.CharField(max_length=100, blank=True)
    amsam_2 = models.CharField(max_length=100, blank=True)
    amsam_3 = models.CharField(max_length=100, blank=True)
    amsam_4 = models.CharField(max_length=100, blank=True)
    amsam_5 = models.CharField(max_length=100, blank=True)
    amsam_empty1 = models.CharField(max_length=100, blank=True)
    amsam_empty2 = models.CharField(max_length=100, blank=True)
    amsam_6 = models.CharField(max_length=100, blank=True)
    amsam_7 = models.CharField(max_length=100, blank=True)
    amsam_empty3 = models.CharField(max_length=100, blank=True)
    amsam_empty4 = models.CharField(max_length=100, blank=True)
    amsam_8 = models.CharField(max_length=100, blank=True)
    amsam_9 = models.CharField(max_length=100, blank=True)
    amsam_10 = models.CharField(max_length=100, blank=True)
    amsam_11 = models.CharField(max_length=100, blank=True)
    amsam_12 = models.CharField(max_length=100, blank=True)
    
    # Physical Attributes
    height_cm = models.CharField(max_length=20, blank=True)
    weight_kg = models.CharField(max_length=20, blank=True)
    complexion = models.CharField(max_length=100, blank=True)
    disability = models.CharField(max_length=200, blank=True, default='No')
    diet = models.CharField(max_length=100, blank=True)
    
    # Education & Career
    education = models.CharField(max_length=200, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    income = models.CharField(max_length=120, blank=True)
    place_of_job = models.CharField(max_length=200, blank=True)
    
    # Family Details
    father_alive = models.BooleanField(default=True)
    mother_alive = models.BooleanField(default=True)
    father_occupation = models.CharField(max_length=200, blank=True)
    mother_occupation = models.CharField(max_length=200, blank=True)
    elder_brothers = models.PositiveIntegerField(default=0)
    younger_brothers = models.PositiveIntegerField(default=0)
    elder_sisters = models.PositiveIntegerField(default=0)
    younger_sisters = models.PositiveIntegerField(default=0)
    native_place = models.CharField(max_length=200, blank=True)
    
    # Location
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True, default='India')
    
    # Personal Details
    marital_status = models.CharField(max_length=80, blank=True, default='Never Married')
    language = models.CharField(max_length=80, blank=True, default='Tamil')
    mother_tongue = models.CharField(max_length=80, blank=True, default='Tamil')
    about = models.TextField(blank=True)
    
    # Partner Expectations
    expected_qualification = models.CharField(max_length=200, blank=True)
    expected_job = models.CharField(max_length=200, blank=True)
    expected_income = models.CharField(max_length=100, blank=True)
    expected_caste = models.CharField(max_length=100, blank=True)
    expected_subcaste = models.CharField(max_length=100, blank=True)
    expected_diet = models.CharField(max_length=100, blank=True)
    expected_marital_status = models.CharField(max_length=100, blank=True)
    other_expectations = models.TextField(blank=True)
    
    # Photos
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    photo2 = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Second Photo")
    
    # Contact Information
    contact_person = models.CharField(max_length=200, blank=True)
    contact_number = models.CharField(max_length=50, blank=True)
    alternate_contact = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    
    # System Fields
    approved = models.BooleanField(default=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_sibling_counts(self):
        counts = {
            'elder_brother': {'married': 0, 'unmarried': 0},
            'younger_brother': {'married': 0, 'unmarried': 0},
            'elder_sister': {'married': 0, 'unmarried': 0},
            'younger_sister': {'married': 0, 'unmarried': 0},
        }
        
        for sibling in self.siblings.all():
            counts[sibling.relationship][sibling.marital_status] += sibling.count
            
        return counts

    def get_total_siblings(self):
        return self.siblings.aggregate(total=models.Sum('count'))['total'] or 0

    # def rasi_cells(self):
    #     data = [getattr(self, f"rasi_{i+1}", "") for i in range(12)]
    #     return self._expand_to_16(data)

    # @property
    # def amsam_cells(self):
    #     data = [getattr(self, f"amsam_{i+1}", "") for i in range(12)]
    #     return self._expand_to_16(data)

    @property
    def rasi_cells(self):
        return [
            self.rasi_1, self.rasi_2, self.rasi_3, self.rasi_4,
            self.rasi_5, self.rasi_empty1, self.rasi_empty2, self.rasi_6,
            self.rasi_7, self.rasi_empty3, self.rasi_empty4, self.rasi_8,
            self.rasi_9, self.rasi_10, self.rasi_11, self.rasi_12,
        ]

    @property
    def amsam_cells(self):
        return [
            self.amsam_1, self.amsam_2, self.amsam_3, self.amsam_4,
            self.amsam_5, self.amsam_empty1, self.amsam_empty2, self.amsam_6,
            self.amsam_7, self.amsam_empty3, self.amsam_empty4, self.amsam_8,
            self.amsam_9, self.amsam_10, self.amsam_11, self.amsam_12,
        ]

    def _expand_to_16(self, data12):
        """Insert empty strings in center 4 positions to make 16 cells"""
        grid16 = []
        insert_positions = {5, 6, 9, 10}  # zero-based index of center blocks
        j = 0
        for i in range(16):
            if i in insert_positions:
                grid16.append("")  # center block empty
            else:
                grid16.append(data12[j])
                j += 1
        return grid16

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # compute age if dob present
        if self.dob and not self.age:
            today = date.today()
            self.age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        if not self.slug:
            base = slugify(self.full_name)
            self.slug = f"{base}-{int(date.today().strftime('%y%m%d%H%M%S'))}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.pk, self.slug])

    def __str__(self): 
        return self.full_name
    
    @property
    def name(self):
        return self.full_name
    
    def get_rasi_data(self):
        """Returns rasi data as a list"""
        return [
            self.rasi_1, self.rasi_2, self.rasi_3, self.rasi_4,
            self.rasi_5, self.rasi_6, self.rasi_7, self.rasi_8,
            self.rasi_9, self.rasi_10, self.rasi_11, self.rasi_12
        ]
    
    def get_amsam_data(self):
        """Returns amsam data as a list"""
        return [
            self.amsam_1, self.amsam_2, self.amsam_3, self.amsam_4,
            self.amsam_5, self.amsam_6, self.amsam_7, self.amsam_8,
            self.amsam_9, self.amsam_10, self.amsam_11, self.amsam_12
        ]
    # @property
    # def rasi_cells(self):
    #     return self.get_rasi_data()

    # @property
    # def amsam_cells(self):
    #     return self.get_amsam_data()


class Company(models.Model):
    name = models.CharField(max_length=200, verbose_name="Company Name")
    logo = models.ImageField(upload_to='company/logo/', blank=True, null=True)
    email = models.EmailField()
    phone1 = models.CharField(max_length=20, verbose_name="Primary Phone")
    phone2 = models.CharField(max_length=20, blank=True, null=True, verbose_name="Secondary Phone")
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Company Details"
    
    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    text = models.TextField()

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title

from django.db import models

# 1. Slider
class Slider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True, null=True)
    image = models.ImageField(upload_to="sliders/")

    def __str__(self):
        return self.title


# 2. Services
class Service(models.Model):
    icon = models.ImageField(upload_to="services/icons/", blank=True, null=True)  
    image = models.ImageField(upload_to="services/images/", blank=True, null=True)  
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300, null=True)
    description = models.TextField()
    link = models.URLField(blank=True)

    def __str__(self):
        return self.title


# 3. Clients
class Client(models.Model):
    image = models.ImageField(upload_to="clients/", blank=True, null=True)
    title = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=300)
    long_desc = models.TextField()

    def __str__(self):
        return self.title


# 4. About
class About(models.Model):
    image1 = models.ImageField(upload_to="about/")
    image2 = models.ImageField(upload_to="about/", blank=True, null=True)
    description = models.TextField()
    long_desc = models.TextField(null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "About Section"


# 5. Contact Us
class Contact(models.Model):
    image = models.ImageField(upload_to="contact/", blank=True, null=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return "Contact Section"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

class SEO(models.Model):
    # Example: "Home Page SEO"
    page_name = models.CharField(max_length=150, unique=True, help_text="Eg: Home, About, Contact")
    
    title = models.TextField(max_length=255, help_text="Meta Title for SEO")
    description = models.TextField(help_text="Meta Description for SEO")
    keywords = models.TextField(help_text="Comma separated keywords")
    iframe_map = models.TextField(blank=True, null=True, help_text="Google Map iframe embed code")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "SEO Setting"
        verbose_name_plural = "SEO Settings"

    def __str__(self):
        return self.page_name
        