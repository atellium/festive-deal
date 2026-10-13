from django.shortcuts import get_object_or_404, render

from offers.models import Business, Category, Location


def home(request):
    selected_location_slug = request.GET.get('location', '')
    selected_category_slug = request.GET.get('category', '')
    selected_location = None
    selected_category = None
    businesses = (
        Business.objects.filter(is_active=True, offer_images__isnull=False)
        .select_related('category')
        .prefetch_related('offer_images', 'locations')
        .distinct()
        .order_by('-is_paid', '-is_verified', 'name')
    )

    if selected_location_slug:
        selected_location = Location.objects.filter(slug=selected_location_slug, is_active=True).first()
        businesses = businesses.filter(locations__slug=selected_location_slug)

    if selected_category_slug:
        selected_category = Category.objects.filter(slug=selected_category_slug).first()
        businesses = businesses.filter(category__slug=selected_category_slug)

    context = {
        'businesses': businesses,
        'categories': Category.objects.all(),
        'locations': Location.objects.filter(is_active=True),
        'selected_category_slug': selected_category_slug,
        'selected_category': selected_category,
        'selected_location_slug': selected_location_slug,
        'selected_location': selected_location,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'core/partials/offer_list.html', context)

    return render(request, 'core/home.html', context)


def business_detail(request, slug):
    business = get_object_or_404(
        Business.objects.prefetch_related('offer_images', 'locations'),
        slug=slug,
        is_active=True,
    )
    return render(request, 'core/business_detail.html', {'business': business})
