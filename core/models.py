# core/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# ---------------------- SiteSettings (Singleton) ----------------------
class SiteSettings(models.Model):
    """تنظیمات کلی سایت - فقط یک رکورد باید وجود داشته باشد."""

    # تصاویر سراسری
    background_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="تصویر پس‌زمینه سایت")
    logo_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="لوگو (هدر و فوتر)")
    about_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="تصویر بخش درباره ما")
    cta_background_image = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="تصویر پس‌زمینه CTA")

     # تنظیمات SEO
    seo_title = models.CharField(
        max_length=255,
        blank=True,
        default="ایزوگام ارومیه | تولید و اجرای ایزوگام | فراز بام",
        verbose_name="عنوان SEO"
    )

    seo_description = models.TextField(
        blank=True,
        default="فراز بام، تولیدکننده و مجری ایزوگام در ارومیه؛ ارائه ایزوگام و خدمات عایق‌کاری رطوبتی با کیفیت و اجرای تخصصی برای پروژه‌های ساختمانی.",
        verbose_name="توضیحات SEO"
    )

    seo_og_image = models.ImageField(
        upload_to='site/seo/',
        blank=True,
        null=True,
        verbose_name="تصویر Open Graph"
    )

    # هیرو
    hero_eyebrow = models.CharField(max_length=120, blank=True, default="برند تخصصی عایق‌کاری رطوبتی", verbose_name="برچسب بالای هیرو")
    hero_brand_name = models.CharField(max_length=80, blank=True, default="فراز بام،", verbose_name="نام برند در عنوان هیرو")
    hero_title = models.CharField(max_length=255, blank=True, default="سپر مطمئن سقف", verbose_name="عنوان برجسته هیرو (بخش رنگی)")
    hero_subtitle = models.CharField(max_length=255, blank=True, default="در برابر آب، گرما و فرسایش", verbose_name="زیرعنوان هیرو (ادامه عنوان)")
    hero_description = models.TextField(blank=True, default="ایزوگام را سیستم مهندسی حفاظت سقف می‌دانیم؛ برای عمر بیشتر سازه، جلوگیری از رطوبت و کیفیت پایدار.", verbose_name="توضیحات هیرو")
    hero_cta_primary_text = models.CharField(max_length=100, blank=True, default="دریافت مشاوره تخصصی", verbose_name="متن دکمه اصلی هیرو")
    hero_cta_secondary_text = models.CharField(max_length=100, blank=True, default="مشاهده نمونه پروژه‌ها", verbose_name="متن دکمه ثانویه هیرو")
    trust_chip_1 = models.CharField(max_length=120, blank=True, default="اجرای اصولی و استاندارد", verbose_name="چیپ اعتماد ۱")
    trust_chip_2 = models.CharField(max_length=120, blank=True, default="دوام بالا در شرایط سخت اقلیمی", verbose_name="چیپ اعتماد ۲")
    trust_chip_3 = models.CharField(max_length=120, blank=True, default="مشاوره متناسب با نوع پروژه", verbose_name="چیپ اعتماد ۳")

    # تماس
    phone_direct = models.CharField(max_length=20, blank=True, default="", verbose_name="شماره تماس مستقیم")
    activity_area = models.CharField(max_length=200, blank=True, default="سراسر کشور", verbose_name="محدوده فعالیت")
    response_time = models.CharField(max_length=100, blank=True, default="کمتر از ۲۴ ساعت", verbose_name="زمان پاسخگویی")

    # فوتر
    footer_brand_name = models.CharField(max_length=80, blank=True, default="فراز بام", verbose_name="نام برند در فوتر")
    footer_tagline = models.CharField(max_length=200, blank=True, default="عایق‌کاری حرفه‌ای سقف", verbose_name="شعار فوتر")
    footer_copyright = models.CharField(max_length=200, default="© تمامی حقوق برای فراز بام محفوظ است.", verbose_name="متن کپی‌رایت فوتر")

    # درباره ما
    about_eyebrow = models.CharField(max_length=120, blank=True, default="درباره برند فراز بام", verbose_name="برچسب بخش درباره ما")
    about_title = models.CharField(max_length=255, blank=True, default="کیفیت، از نگاه مهندسی تا اجرا", verbose_name="عنوان درباره ما")
    about_text1 = models.TextField(blank=True, default="", verbose_name="پاراگراف اول درباره ما")
    about_text2 = models.TextField(blank=True, default="", verbose_name="پاراگراف دوم درباره ما")
    about_quality_core_title = models.CharField(max_length=100, blank=True, default="کیفیت", verbose_name="عنوان دایره کیفیت")
    about_quality_core_text = models.TextField(blank=True, default="هسته اصلی", verbose_name="متن دایره کیفیت")
    about_badge_num = models.CharField(max_length=20, blank=True, default="۱۵+", verbose_name="عدد نشان درباره ما")
    about_badge_label = models.CharField(max_length=80, blank=True, default="سال تجربه", verbose_name="برچسب نشان درباره ما")
    about_stat_1_value = models.CharField(max_length=30, blank=True, default="۱۲۰۰+", verbose_name="آمار کوچک ۱ (عدد)")
    about_stat_1_label = models.CharField(max_length=80, blank=True, default="پروژه موفق", verbose_name="آمار کوچک ۱ (برچسب)")
    about_stat_2_value = models.CharField(max_length=30, blank=True, default="۹۸٪", verbose_name="آمار کوچک ۲ (عدد)")
    about_stat_2_label = models.CharField(max_length=80, blank=True, default="رضایت مشتری", verbose_name="آمار کوچک ۲ (برچسب)")
    about_stat_3_value = models.CharField(max_length=30, blank=True, default="۲۴/۷", verbose_name="آمار کوچک ۳ (عدد)")
    about_stat_3_label = models.CharField(max_length=80, blank=True, default="پشتیبانی", verbose_name="آمار کوچک ۳ (برچسب)")

    # عناوین سکشن‌ها
    stats_eyebrow = models.CharField(max_length=120, blank=True, default="دستاوردهای فراز بام", verbose_name="برچسب بخش آمار")
    stats_title = models.CharField(max_length=200, blank=True, default="اعداد، روایت‌گر کیفیت ماست", verbose_name="عنوان بخش آمار")
    stats_desc = models.TextField(blank=True, default="هر عدد پشت آن سال‌ها تجربه، پروژه‌های موفق و اعتماد مشتریان است.", verbose_name="توضیح بخش آمار")

    products_eyebrow = models.CharField(max_length=120, blank=True, default="محصولات", verbose_name="برچسب بخش محصولات")
    products_title = models.CharField(max_length=200, blank=True, default="راه‌حل‌های عایق‌کاری متنوع", verbose_name="عنوان بخش محصولات")
    products_desc = models.TextField(blank=True, default="محصولات متناسب با نوع سقف، کاربری و شرایط اقلیمی.", verbose_name="توضیح بخش محصولات")

    team_eyebrow = models.CharField(max_length=120, blank=True, default="تیم ما", verbose_name="برچسب بخش تیم")
    team_title = models.CharField(max_length=200, blank=True, default="متخصصان فراز بام", verbose_name="عنوان بخش تیم")
    team_desc = models.TextField(blank=True, default="تیمی از مهندسان و اجراکنندگان با تجربه در عایق‌کاری سقف.", verbose_name="توضیح بخش تیم")

    videos_eyebrow = models.CharField(max_length=120, blank=True, default="ویدیوها", verbose_name="برچسب بخش ویدیو")
    videos_title = models.CharField(max_length=200, blank=True, default="فرآیند اجرا را ببینید", verbose_name="عنوان بخش ویدیو")
    videos_desc = models.TextField(blank=True, default="نمونه‌های واقعی از اجرای پروژه‌های عایق‌کاری.", verbose_name="توضیح بخش ویدیو")

    features_eyebrow = models.CharField(max_length=120, blank=True, default="مزایا", verbose_name="برچسب بخش مزایا")
    features_title = models.CharField(max_length=200, blank=True, default="چرا فراز بام؟", verbose_name="عنوان بخش مزایا")
    features_desc = models.TextField(blank=True, default="مزایای همکاری با ما در یک نگاه.", verbose_name="توضیح بخش مزایا")

    services_eyebrow = models.CharField(max_length=120, blank=True, default="خدمات", verbose_name="برچسب بخش خدمات")
    services_title = models.CharField(max_length=200, blank=True, default="خدمات تخصصی عایق‌کاری", verbose_name="عنوان بخش خدمات")
    services_desc = models.TextField(blank=True, default="از مشاوره تا اجرا و پشتیبانی.", verbose_name="توضیح بخش خدمات")

    anatomy_eyebrow = models.CharField(max_length=120, blank=True, default="ساختار لایه‌ای ایزوگام", verbose_name="برچسب بخش آناتومی")
    anatomy_title = models.CharField(max_length=200, blank=True, default="هر لایه، یک نقش حیاتی در ماندگاری نهایی", verbose_name="عنوان بخش آناتومی")
    anatomy_desc = models.TextField(blank=True, default="کیفیت ایزوگام تنها به ظاهر آن محدود نیست. عملکرد نهایی، حاصل همکاری چند لایه مکمل است.", verbose_name="توضیح بخش آناتومی")
    anatomy_hint_1 = models.TextField(blank=True, default="روی هر لایه توقف کنید تا عملکرد دقیق آن را ببینید.", verbose_name="راهنمای آناتومی ۱")
    anatomy_hint_2 = models.TextField(blank=True, default="با اسکرول، فاصله لایه‌ها نمایان می‌شود تا ساختار درونی را بهتر درک کنید.", verbose_name="راهنمای آناتومی ۲")
    anatomy_hint_3 = models.TextField(blank=True, default="این ساختار چندلایه همان چیزی است که از سازه در برابر نفوذ و فرسایش محافظت می‌کند.", verbose_name="راهنمای آناتومی ۳")

    process_eyebrow = models.CharField(max_length=120, blank=True, default="فرآیند همکاری", verbose_name="برچسب بخش فرآیند")
    process_title = models.CharField(max_length=200, blank=True, default="از مشاوره تا تحویل پروژه", verbose_name="عنوان بخش فرآیند")
    process_desc = models.TextField(blank=True, default="مسیر شفاف و مرحله‌به‌مرحله برای اجرای پروژه شما.", verbose_name="توضیح بخش فرآیند")

    projects_eyebrow = models.CharField(max_length=120, blank=True, default="نمونه کارها", verbose_name="برچسب بخش پروژه‌ها")
    projects_title = models.CharField(max_length=200, blank=True, default="پروژه‌های اجراشده", verbose_name="عنوان بخش پروژه‌ها")
    projects_desc = models.TextField(blank=True, default="نمونه‌هایی از پروژه‌های موفق عایق‌کاری.", verbose_name="توضیح بخش پروژه‌ها")

    gallery_eyebrow = models.CharField(max_length=120, blank=True, default="گالری", verbose_name="برچسب بخش گالری")
    gallery_title = models.CharField(max_length=200, blank=True, default="تصاویر پروژه‌ها", verbose_name="عنوان بخش گالری")
    gallery_desc = models.TextField(blank=True, default="گالری تصاویر از اجرای پروژه‌های مختلف.", verbose_name="توضیح بخش گالری")

    faq_eyebrow = models.CharField(max_length=120, blank=True, default="سوالات متداول", verbose_name="برچسب بخش FAQ")
    faq_title = models.CharField(max_length=200, blank=True, default="پاسخ به پرسش‌های رایج", verbose_name="عنوان بخش FAQ")
    faq_desc = models.TextField(blank=True, default="پاسخ سوالات متداول درباره عایق‌کاری و خدمات ما.", verbose_name="توضیح بخش FAQ")

    contact_eyebrow = models.CharField(max_length=120, blank=True, default="تماس با ما", verbose_name="برچسب بخش تماس")
    contact_title = models.CharField(max_length=200, blank=True, default="درخواست مشاوره رایگان", verbose_name="عنوان بخش تماس")
    contact_desc = models.TextField(blank=True, default="فرم زیر را پر کنید تا در اسرع وقت با شما تماس بگیریم.", verbose_name="توضیح بخش تماس")
    contact_info_title = models.CharField(max_length=200, blank=True, default="اطلاعات تماس", verbose_name="عنوان باکس اطلاعات تماس")
    contact_info_text = models.TextField(blank=True, default="برای مشاوره تخصصی و بازدید از محل پروژه با ما در تماس باشید.", verbose_name="متن باکس اطلاعات تماس")
    contact_form_title = models.CharField(max_length=200, blank=True, default="فرم درخواست", verbose_name="عنوان فرم تماس")
    contact_form_desc = models.TextField(blank=True, default="اطلاعات پروژه خود را وارد کنید.", verbose_name="توضیح فرم تماس")

    cta_title = models.CharField(max_length=200, blank=True, default="آماده شروع پروژه عایق‌کاری هستید؟", verbose_name="عنوان CTA")
    cta_desc = models.TextField(blank=True, default="همین حالا درخواست مشاوره رایگان ثبت کنید.", verbose_name="توضیح CTA")
    cta_btn_primary = models.CharField(max_length=100, blank=True, default="ثبت درخواست", verbose_name="متن دکمه اصلی CTA")
    cta_btn_secondary = models.CharField(max_length=100, blank=True, default="تماس مستقیم", verbose_name="متن دکمه ثانویه CTA")
    
    class Meta:
        verbose_name = "تنظیمات سایت"
        verbose_name_plural = "تنظیمات سایت"

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError("فقط یک نمونه از تنظیمات سایت می‌تواند وجود داشته باشد.")
        super().save(*args, **kwargs)

    def __str__(self):
        return "تنظیمات سایت"


# ---------------------- Stat ----------------------
class Stat(models.Model):
    number = models.IntegerField(verbose_name="عدد آمار")
    label = models.CharField(max_length=200, verbose_name="توضیح آمار")
    cover_image = models.ImageField(upload_to='stats/', blank=True, null=True, verbose_name="تصویر کاور")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")


    class Meta:
        verbose_name = "آمار"
        verbose_name_plural = "آمارها"
        ordering = ['order']

    def __str__(self):
        return f"{self.number} - {self.label}"


# ---------------------- About Bullet ----------------------
class AboutBullet(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان گلوله")
    text = models.TextField(verbose_name="متن گلوله")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "گلوله درباره ما"
        verbose_name_plural = "گلوله‌های درباره ما"
        ordering = ['order']

    def __str__(self):
        return self.title


# ---------------------- Feature ----------------------
class Feature(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان مزیت")
    description = models.TextField(verbose_name="توضیح مزیت")
    svg_icon = models.TextField(verbose_name="کد SVG آیکون", help_text="کد SVG کامل (مثلاً <svg>...</svg>)")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "مزیت"
        verbose_name_plural = "مزایا"
        ordering = ['order']

    def __str__(self):
        return self.title


# ---------------------- Service & ServiceItem ----------------------
class Service(models.Model):
    index = models.CharField(max_length=10, verbose_name="شماره سرویس (مثلاً 01)")
    title = models.CharField(max_length=150, verbose_name="عنوان سرویس")
    description = models.TextField(verbose_name="توضیح سرویس")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"
        ordering = ['order']

    def __str__(self):
        return f"{self.index} - {self.title}"


class ServiceItem(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='items', verbose_name="خدمت")
    text = models.CharField(max_length=200, verbose_name="متن آیتم")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "آیتم خدمت"
        verbose_name_plural = "آیتم‌های خدمات"
        ordering = ['order']

    def __str__(self):
        return self.text


# ---------------------- Anatomy Layer ----------------------
ANATOMY_LAYER_DEPTHS = {
    '1': 250,
    '2': 100,
    '3': -50,
    '4': -200,
}


class AnatomyLayer(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام لایه")
    info_text = models.TextField(verbose_name="توضیح لایه")
    depth = models.IntegerField(
        verbose_name="عمق انیمیشن",
        help_text="خودکار از شناسه لایه (۱ تا ۴) تنظیم می‌شود.",
        editable=False,
    )
    info_id = models.CharField(
        max_length=10,
        verbose_name="شناسه لایه",
        help_text="فقط ۱، ۲، ۳ یا ۴ — رنگ و عمق ۳D بر اساس این شناسه است.",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        verbose_name = "لایه ایزوگام"
        verbose_name_plural = "لایه‌های ایزوگام"
        ordering = ['order', 'info_id']

    def __str__(self):
        return self.name

    @property
    def animation_depth(self):
        return ANATOMY_LAYER_DEPTHS.get(str(self.info_id), self.depth)

    @property
    def css_class(self):
        return f"layer-{self.info_id}"

    def save(self, *args, **kwargs):
        mapped = ANATOMY_LAYER_DEPTHS.get(str(self.info_id))
        if mapped is not None:
            self.depth = mapped
        super().save(*args, **kwargs)


# ---------------------- Process Step ----------------------
class ProcessStep(models.Model):
    step_number = models.CharField(max_length=10, verbose_name="شماره مرحله (مثلاً 01)")
    title = models.CharField(max_length=150, verbose_name="عنوان مرحله")
    description = models.TextField(verbose_name="توضیح مرحله")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        verbose_name = "مرحله همکاری"
        verbose_name_plural = "مراحل همکاری"
        ordering = ['order']

    def __str__(self):
        return f"{self.step_number} - {self.title}"


# ---------------------- Project (قبلاً وجود داشت) ----------------------
class Project(models.Model):
    STATUS_CHOICES = [
        ('done', 'تحویل شده'),
        ('progress', 'در دست اجرا'),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان پروژه")
    description = models.TextField(verbose_name="توضیحات")
    project_type = models.CharField(max_length=100, verbose_name="نوع کاربری")  # مسکونی/تجاری/صنعتی
    surface_type = models.CharField(max_length=100, blank=True, verbose_name="سطح اجرا")  # بام/سقف/سوله
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='done', verbose_name="وضعیت")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="تصویر")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return self.title


# ---------------------- FAQ ----------------------
class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ['order']
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"

    def __str__(self):
        return self.question


# ---------------------- Contact Message ----------------------
class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    city = models.CharField(max_length=100, verbose_name="شهر")
    project_type = models.CharField(max_length=100, verbose_name="نوع پروژه")
    message = models.TextField(verbose_name="توضیح پروژه")
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name="پردازش شده")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f'{self.full_name} - {self.phone}'


# ---------------------- Product ----------------------
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات محصول")
    features = models.TextField(verbose_name="ویژگی‌ها", help_text="هر ویژگی را در یک خط بنویسید", blank=True)
    thickness = models.CharField(max_length=50, blank=True, verbose_name="ضخامت")
    weight = models.CharField(max_length=50, blank=True, verbose_name="وزن")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر محصول")
    is_featured = models.BooleanField(default=False, verbose_name="محصول ویژه")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


# ---------------------- Team Member ----------------------
class TeamMember(models.Model):
    name = models.CharField(max_length=150, verbose_name="نام")
    role = models.CharField(max_length=150, verbose_name="سمت")
    bio = models.TextField(blank=True, verbose_name="بیوگرافی کوتاه")
    photo = models.ImageField(upload_to='team/', blank=True, null=True, verbose_name="عکس")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

    def __str__(self):
        return f"{self.name} — {self.role}"


# ---------------------- Media Item ----------------------
class MediaItem(models.Model):
    MEDIA_TYPES = [
        ('image', 'عکس'),
        ('video', 'ویدیو'),
    ]
    title = models.CharField(max_length=200, verbose_name="عنوان")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image', verbose_name="نوع رسانه")
    image = models.ImageField(upload_to='gallery/', verbose_name="تصویر / پوستر ویدیو")
    video_url = models.URLField(blank=True, verbose_name="لینک ویدیو", help_text="لینک YouTube یا Aparat")
    caption = models.TextField(blank=True, verbose_name="توضیح")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")
    is_featured = models.BooleanField(default=False, verbose_name="برجسته (سایز بزرگ)")

    class Meta:
        ordering = ['order', '-id']
        verbose_name = "رسانه"
        verbose_name_plural = "گالری رسانه"

    def __str__(self):
        return self.title

