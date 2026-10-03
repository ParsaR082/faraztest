# core/views.py
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib import messages
from .models import (
    SiteSettings, Stat, AboutBullet, Feature,
    Service, AnatomyLayer, ProcessStep,
    Project, FAQ, Product, TeamMember, MediaItem
)
from .forms import ContactForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Singleton settings
        context['site_settings'] = SiteSettings.objects.first()

        # Stats
        context['stats'] = Stat.objects.all()

        # Products
        products = Product.objects.all()
        for product in products:
            if product.features:
                product.features_list = product.features.splitlines()
            else:
                product.features_list = []
        context['products'] = products

        # About bullets
        context['about_bullets'] = AboutBullet.objects.all()

        # Features
        context['features'] = Feature.objects.all()

        # Services with related items (پیش‌واکشی آیتم‌ها)
        context['services'] = Service.objects.prefetch_related('items').all()

        # Anatomy layers — always ordered 1→4 for stable 3D stack
        context['anatomy_layers'] = AnatomyLayer.objects.order_by('order', 'info_id')[:4]

        # Process steps
        context['process_steps'] = ProcessStep.objects.all()

        # Projects
        context['projects'] = Project.objects.all()

        # FAQs
        context['faqs'] = FAQ.objects.all()

        # Team members
        context['team_members'] = TeamMember.objects.filter(is_active=True)

        # Media gallery
        context['media_items'] = MediaItem.objects.all()
        context['video_items'] = MediaItem.objects.filter(media_type='video')
        context['gallery_images'] = MediaItem.objects.filter(media_type='image')

        # Contact form
        if 'contact_form' not in context:
            context['contact_form'] = ContactForm()

        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'درخواست شما با موفقیت ثبت شد. به زودی با شما تماس می‌گیریم.')
            return redirect('/#contact')
        else:
            context = self.get_context_data()
            context['contact_form'] = form
            return self.render_to_response(context)