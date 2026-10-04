# core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Stat, AboutBullet, Feature,
    Service, ServiceItem, AnatomyLayer, ProcessStep,
    Project, FAQ, ContactMessage, Product, TeamMember, MediaItem
)


# ---------- Inline ها ----------
class ServiceItemInline(admin.TabularInline):
    model = ServiceItem
    extra = 1
    fields = ('text', 'order')


# ---------- SiteSettings (Singleton) ----------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("تصاویر سراسری", {
            'fields': ('background_image', 'logo_image', 'about_image', 'cta_background_image'),
        }),
        ("تنظیمات SEO", {
            'fields': ('seo_title', 'seo_description', 'seo_og_image'),
        }),
        ("بخش هیرو", {
            'fields': (
                'hero_eyebrow', 'hero_brand_name', 'hero_title', 'hero_subtitle', 'hero_description',
                'hero_cta_primary_text', 'hero_cta_secondary_text',
                'trust_chip_1', 'trust_chip_2', 'trust_chip_3',
            )
        }),
        ("اطلاعات تماس", {
            'fields': ('phone_direct', 'activity_area', 'response_time')
        }),
        ("بخش درباره ما", {
            'fields': (
                'about_eyebrow', 'about_title', 'about_text1', 'about_text2',
                'about_quality_core_title', 'about_quality_core_text',
                'about_badge_num', 'about_badge_label',
                'about_stat_1_value', 'about_stat_1_label',
                'about_stat_2_value', 'about_stat_2_label',
                'about_stat_3_value', 'about_stat_3_label',
            )
        }),
        ("عناوین بخش آمار", {
            'fields': ('stats_eyebrow', 'stats_title', 'stats_desc'),
        }),
        ("عناوین بخش محصولات", {
            'fields': ('products_eyebrow', 'products_title', 'products_desc'),
        }),
        ("عناوین بخش تیم", {
            'fields': ('team_eyebrow', 'team_title', 'team_desc'),
        }),
        ("عناوین بخش ویدیو", {
            'fields': ('videos_eyebrow', 'videos_title', 'videos_desc'),
        }),
        ("عناوین بخش مزایا", {
            'fields': ('features_eyebrow', 'features_title', 'features_desc'),
        }),
        ("عناوین بخش خدمات", {
            'fields': ('services_eyebrow', 'services_title', 'services_desc'),
        }),
        ("بخش آناتومی (متن)", {
            'fields': (
                'anatomy_eyebrow', 'anatomy_title', 'anatomy_desc',
                'anatomy_hint_1', 'anatomy_hint_2', 'anatomy_hint_3',
            ),
        }),
        ("عناوین بخش فرآیند", {
            'fields': ('process_eyebrow', 'process_title', 'process_desc'),
        }),
        ("عناوین بخش پروژه‌ها", {
            'fields': ('projects_eyebrow', 'projects_title', 'projects_desc'),
        }),
        ("عناوین بخش گالری", {
            'fields': ('gallery_eyebrow', 'gallery_title', 'gallery_desc'),
        }),
        ("عناوین بخش FAQ", {
            'fields': ('faq_eyebrow', 'faq_title', 'faq_desc'),
        }),
        ("بخش تماس (متن)", {
            'fields': (
                'contact_eyebrow', 'contact_title', 'contact_desc',
                'contact_info_title', 'contact_info_text',
                'contact_form_title', 'contact_form_desc',
            ),
        }),
        ("بنر CTA", {
            'fields': ('cta_title', 'cta_desc', 'cta_btn_primary', 'cta_btn_secondary'),
        }),
        ("فوتر", {
            'fields': ('footer_brand_name', 'footer_tagline', 'footer_copyright'),
        }),
    )

    def has_add_permission(self, request):
        # اگر از قبل وجود دارد، اجازه اضافه نده
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # اجازه حذف نده
        return False

    # مخفی کردن دکمه حذف در فرم
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


# ---------- Stat ----------
@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('number', 'label', 'order')
    list_editable = ('order',)


# ---------- About Bullet ----------
@admin.register(AboutBullet)
class AboutBulletAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)


# ---------- Feature ----------
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'svg_preview')
    list_editable = ('order',)
    readonly_fields = ('svg_preview',)

    def svg_preview(self, obj):
        if obj.svg_icon:
            return format_html('<div style="max-width:50px; max-height:50px;">{}</div>', obj.svg_icon)
        return "-"
    svg_preview.short_description = "پیش‌نمایش SVG"


# ---------- Service ----------
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('index', 'title', 'order')
    list_editable = ('order',)
    inlines = [ServiceItemInline]


# ---------- Anatomy Layer ----------
@admin.register(AnatomyLayer)
class AnatomyLayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'info_id', 'depth', 'order')
    list_editable = ('order', 'info_id')
    readonly_fields = ('depth',)


# ---------- Process Step ----------
@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')
    list_editable = ('order',)


# ---------- Project ----------
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'surface_type', 'status', 'created_at')
    list_filter = ('project_type', 'status')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)


# ---------- FAQ ----------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question', 'answer')


# ---------- Contact Message ----------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'project_type', 'created_at', 'is_processed')
    list_filter = ('is_processed', 'project_type')
    search_fields = ('full_name', 'phone', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_processed']

    @admin.action(description='علامت‌گذاری به‌عنوان پردازش شده')
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(is_processed=True)
        self.message_user(request, f'{updated} پیام با موفقیت علامت‌گذاری شد.')


# ---------- Product ----------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_featured', 'thickness', 'weight', 'order', 'created_at')
    list_editable = ('order', 'is_featured')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('name', 'description', 'features')
    readonly_fields = ('created_at',)
    fieldsets = (
        ("اطلاعات اصلی", {
            'fields': ('name', 'description', 'is_featured', 'order')
        }),
        ("ویژگی‌ها و مشخصات", {
            'fields': ('features', 'thickness', 'weight')
        }),
        ("تصویر", {
            'fields': ('image',)
        }),
        ("اطلاعات سیستم", {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# ---------- Team Member ----------
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'role', 'bio')


# ---------- Media Item ----------
@admin.register(MediaItem)
class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'is_featured', 'order')
    list_editable = ('order', 'is_featured')
    list_filter = ('media_type', 'is_featured')
    search_fields = ('title', 'caption')