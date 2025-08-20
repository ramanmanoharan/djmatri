from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Profile, Subcaste, Company, Service, Review, BlogPost, Profile, About, Contact, Slider
from .forms import FilterForm, ContactForm

def home(request):
    sliders = Slider.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.all()
    recent_profiles = Profile.objects.filter(approved=True)[:12]
    blogs = BlogPost.objects.order_by('-date')[:3]
    form = FilterForm(request.GET or None)
    return render(request, 'home.html', {
        'sliders': sliders,
        'services': services,
        'reviews': reviews,
        'recent_profiles': recent_profiles,
        'blogs': blogs,
        'form': form,
    })


def profile_list(request, gender_filter=None):
    company = Company.objects.first()

    qs = Profile.objects.filter(approved=True).select_related(
        "gender", "caste", "subcaste"
    ).order_by("-created_at")

    # ✅ Apply gender filter if given
    if gender_filter:
        qs = qs.filter(gender__name__iexact=gender_filter)

    # --- Normal filters (form) ---
    form = FilterForm(request.GET or None)
    if form.is_valid() and any(form.cleaned_data.values()):
        gender = form.cleaned_data.get("gender")
        caste = form.cleaned_data.get("caste")
        subcaste = form.cleaned_data.get("subcaste")
        age_min = form.cleaned_data.get("age_min")
        age_max = form.cleaned_data.get("age_max")

        if gender:
            qs = qs.filter(gender=gender)
        if caste:
            qs = qs.filter(caste=caste)
        if subcaste:
            qs = qs.filter(subcaste=subcaste)
        if age_min:
            qs = qs.filter(age__gte=age_min)
        if age_max:
            qs = qs.filter(age__lte=age_max)

    # --- Search ---
    search_query = request.GET.get("search", "").strip()
    if search_query:
        qs = qs.filter(
            Q(full_name__icontains=search_query)
            | Q(caste__name__icontains=search_query)
            | Q(subcaste__name__icontains=search_query)
            | Q(city__icontains=search_query)
            | Q(occupation__icontains=search_query)
        )

    # --- Pagination ---
    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profiles/list.html",
        {
            "form": form,
            "page_obj": page_obj,
            "company": company,
            "search_query": search_query,
            "gender_filter": gender_filter,
        },
    )

def profile_detail(request, pk, slug):
    profile = get_object_or_404(
        Profile.objects.select_related('gender', 'caste', 'subcaste')
                      .prefetch_related('siblings'),
        pk=pk,
        slug=slug,
        approved=True
    )
    
    # Get company details
    company = Company.objects.first()
    
    # Get sibling counts
    sibling_counts = profile.get_sibling_counts()
    
    # Photo switching logic
    show_photo1 = True
    if 'show_photo1' in request.session:
        show_photo1 = request.session['show_photo1']
    
    if request.GET.get('switch_photos') == '1':
        show_photo1 = not show_photo1
        request.session['show_photo1'] = show_photo1
    
    context = {
        'profile': profile,
        'company': company,
        'sibling_counts': sibling_counts,
        'show_photo1': show_photo1,
    }
    
    return render(request, 'profiles/detail.html', context)


def subcastes_api(request, caste_id):
    subcastes = Subcaste.objects.filter(caste_id=caste_id).order_by('name')
    data = [{'id': sc.id, 'name': sc.name} for sc in subcastes]
    return JsonResponse({'results': data})

def about_page(request):
    about = About.objects.first()  # only one about section
    return render(request, 'profiles/about.html', {'about': about})

def contact_page(request):
    contact = Contact.objects.first()
    return render(request, 'profiles/contact.html', {'contact': contact})

def male_profiles(request):
    return profile_list(request, gender_filter="Male")

def female_profiles(request):
    return profile_list(request, gender_filter="Female")

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "service_detail.html", {"service": service})

def profile_search(request):
    """Search form மட்டும் காட்டும் page"""
    form = FilterForm(request.GET or None)
    if request.GET and form.is_valid():
        # valid search submit பண்ணினா → listing pageக்கு redirect
        return redirect('/profiles/?' + request.META['QUERY_STRING'])
    return render(request, "profiles/search.html", {"form": form})

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "profiles/contact.html", {"form": form})
