from .models import Company, SEO

def company_details(request):
    try:
        company = Company.objects.first()
    except:
        company = None
    return {'company': company}


def seo_context(request):
    seo = None
    try:
        # Example: load default SEO for "Home"
        seo = SEO.objects.filter(page_name="Home").first()
    except:
        pass
    return {"seo": seo}