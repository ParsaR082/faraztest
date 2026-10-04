from django.core.management.base import BaseCommand

from core.models import (
    SiteSettings, Stat, AboutBullet, Feature, Service, ServiceItem,
    AnatomyLayer, ProcessStep, FAQ, Product, TeamMember, MediaItem, Project,
)


class Command(BaseCommand):
    help = 'Seed default site content for admin-managed homepage'

    def handle(self, *args, **options):
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write('Created SiteSettings')

        defaults = {
            'seo_title': 'ایزوگام ارومیه | تولید و اجرای ایزوگام | فراز بام',
            'seo_description': (
                'فراز بام، تولیدکننده و مجری ایزوگام در ارومیه؛ ارائه ایزوگام و خدمات '
                'عایق‌کاری رطوبتی با کیفیت و اجرای تخصصی برای پروژه‌های ساختمانی.'
            ),

            'hero_eyebrow': 'برند تخصصی عایق‌کاری رطوبتی',
            'hero_brand_name': 'فراز بام،',
            'hero_title': 'تولید و اجرای ایزوگام در ارومیه',
            'hero_subtitle': 'عایق‌کاری رطوبتی تخصصی برای ساختمان',
            'hero_description': (
                'ایزوگام را سیستم مهندسی حفاظت سقف می‌دانیم؛ برای عمر بیشتر سازه، '
                'جلوگیری از رطوبت و کیفیت پایدار.'
            ),
            'hero_cta_primary_text': 'دریافت مشاوره تخصصی',
            'hero_cta_secondary_text': 'مشاهده نمونه پروژه‌ها',
            'trust_chip_1': 'اجرای اصولی و استاندارد',
            'trust_chip_2': 'دوام بالا در شرایط سخت اقلیمی',
            'trust_chip_3': 'مشاوره متناسب با نوع پروژه',
            'phone_direct': '۰۹۱۲ ۰۰۰ ۰۰۰۰',
            'activity_area': 'اجرای پروژه‌های مسکونی، تجاری و صنعتی',
            'response_time': 'هماهنگی و پیگیری در سریع‌ترین زمان ممکن',
            'footer_brand_name': 'فراز بام',
            'footer_tagline': 'عایق‌کاری تخصصی',
            'footer_copyright': '© تمامی حقوق برای فراز بام محفوظ است.',
            'about_eyebrow': 'درباره برند فراز بام',
            'about_title': 'از اجرای ساده تا راهکار مهندسی‌شده برای حفاظت ماندگار',
            'about_text1': (
                'فراز بام با تمرکز بر تولید و اجرای ایزوگام و ارائه راهکارهای عایق‌کاری رطوبتی در ارومیه فعالیت می‌کند. '
                'در هر پروژه، شرایط سطح، شیب، اقلیم و نوع کاربری بررسی می‌شود تا مناسب‌ترین راهکار عایق‌کاری انتخاب شود.'
            ),
            'about_text2': (
                'این رویکرد به اجرای دقیق‌تر ایزوگام، کاهش ریسک نفوذ رطوبت و افزایش دوام عایق در برابر شرایط مختلف آب‌وهوایی کمک می‌کند.'
            ),
            'about_quality_core_title': 'کیفیت',
            'about_quality_core_text': 'هسته اصلی',
            'about_badge_num': '۱۵+',
            'about_badge_label': 'سال تجربه',
            'about_stat_1_value': '۱۲۰۰+',
            'about_stat_1_label': 'پروژه اجرا شده',
            'about_stat_2_value': '۹۸٪',
            'about_stat_2_label': 'رضایت مشتری',
            'about_stat_3_value': '۲۴/۷',
            'about_stat_3_label': 'پشتیبانی',
            'stats_eyebrow': 'دستاوردهای فراز بام',
            'stats_title': 'اعداد، روایت‌گر کیفیت ماست',
            'stats_desc': 'هر عدد پشت آن سال‌ها تجربه، پروژه‌های موفق و اعتماد مشتریان است.',
            'products_eyebrow': 'محصولات فراز بام',
            'products_title': 'ایزوگام‌های باکیفیت و مقاوم برای انواع پروژه‌ها',
            'products_desc': (
                'محصولات ما با استفاده از بهترین متریال و تکنولوژی روز تولید می‌شوند تا بالاترین سطح '
                'حفاظت را در برابر رطوبت، گرما و فرسایش ارائه دهند.'
            ),
            'team_eyebrow': 'تیم فراز بام',
            'team_title': 'متخصصانی که پشت کیفیت می‌ایستند',
            'team_desc': 'تیمی از مهندسان، کارشناسان فنی و اجراکنندگان با تجربه در عایق‌کاری سقف.',
            'videos_eyebrow': 'ویدیوهای کارخانه',
            'videos_title': 'فرآیند تولید و اجرا را از نزدیک ببینید',
            'videos_desc': 'نمونه‌های واقعی از خط تولید و اجرای پروژه‌های عایق‌کاری.',
            'features_eyebrow': 'مزیت‌های کلیدی',
            'features_title': 'چرا فراز بام انتخاب می‌شود؟',
            'features_desc': 'مزایای همکاری با ما در یک نگاه.',
            'services_eyebrow': 'خدمات فراز بام',
            'services_title': 'خدمات تخصصی ایزوگام و عایق‌کاری',
            'services_desc': 'از مشاوره و بازدید تا اجرا و پشتیبانی.',
            'anatomy_eyebrow': 'ساختار لایه‌ای ایزوگام',
            'anatomy_title': 'هر لایه، یک نقش حیاتی در ماندگاری نهایی',
            'anatomy_desc': (
                'کیفیت ایزوگام تنها به ظاهر آن محدود نیست. عملکرد نهایی، حاصل همکاری چند لایه مکمل است '
                'که هر کدام در برابر رطوبت، کشش، تابش و اتصال به سطح نقش کلیدی دارند.'
            ),
            'anatomy_hint_1': 'روی هر لایه توقف کنید تا عملکرد دقیق آن را ببینید.',
            'anatomy_hint_2': 'با اسکرول، فاصله لایه‌ها نمایان می‌شود تا ساختار درونی را بهتر درک کنید.',
            'anatomy_hint_3': 'این ساختار چندلایه همان چیزی است که از سازه در برابر نفوذ و فرسایش محافظت می‌کند.',
            'process_eyebrow': 'فرآیند همکاری',
            'process_title': 'مراحل سفارش و اجرای ایزوگام',
            'process_desc': 'از مشاوره و بازدید اولیه تا اجرای تخصصی و تحویل نهایی پروژه.',
            'projects_eyebrow': 'کارخانه فراز بام',
            'projects_title': 'گالری کارخانه و فرآیند تولید ایزوگام',
            'projects_desc': 'نگاهی به بخش‌های مختلف کارخانه، خط تولید و فرآیند آماده‌سازی و تولید ایزوگام در مجموعه فراز بام.',
            'gallery_eyebrow': 'گالری کارخانه',
            'gallery_title': 'تصاویر از خط تولید و پروژه‌ها',
            'gallery_desc': 'گالری تصاویر از اجرای پروژه‌های مختلف و فضای تولید.',
            'faq_eyebrow': 'سوالات متداول',
            'faq_title': 'پاسخ به پرسش‌های رایج مشتریان',
            'faq_desc': 'این سوالات به تصمیم‌گیری سریع‌تر کارفرما کمک می‌کنند.',
            'contact_eyebrow': 'تماس با فراز بام',
            'contact_title': 'برای دریافت مشاوره و بررسی پروژه با ما در ارتباط باشید',
            'contact_desc': (
                'اگر پروژه شما نیاز به بازدید، بررسی فنی، برآورد اولیه یا انتخاب بهترین راهکار عایق‌کاری دارد، '
                'اطلاعات خود را ثبت کنید تا در سریع‌ترین زمان با شما تماس بگیریم.'
            ),
            'contact_info_title': 'اطلاعات تماس',
            'contact_info_text': 'برای مشاوره تخصصی و بازدید از محل پروژه با ما در تماس باشید.',
            'contact_form_title': 'درخواست کارشناسی پروژه',
            'contact_form_desc': 'فرم زیر را تکمیل کنید تا با توجه به نوع پروژه، مشاوره اولیه ارائه شود.',
            'cta_title': 'آماده شروع پروژه عایق‌کاری هستید؟',
            'cta_desc': 'همین حالا درخواست مشاوره رایگان ثبت کنید.',
            'cta_btn_primary': 'ثبت درخواست تماس',
            'cta_btn_secondary': 'تماس مستقیم',
        }
        for key, value in defaults.items():
            setattr(settings, key, value)
        settings.save()

        self._seed_stats()
        self._seed_about_bullets()
        self._seed_anatomy()
        self._seed_process()
        self._seed_faqs()
        self.stdout.write(self.style.SUCCESS('Site content seeded successfully.'))

    def _seed_stats(self):
        if Stat.objects.exists():
            return
        stats = [
            (15, 'سال تجربه در اجرای پروژه‌های عایق‌کاری', 1),
            (1200, 'پروژه اجرا شده در مقیاس مسکونی، تجاری و صنعتی', 2),
            (98, 'درصد رضایت مشتریان و بازگشت برای پروژه‌های بعدی', 3),
            (24, 'پاسخگویی و مشاوره در سریع‌ترین زمان ممکن', 4),
        ]
        for number, label, order in stats:
            Stat.objects.create(number=number, label=label, order=order)

    def _seed_about_bullets(self):
        if AboutBullet.objects.exists():
            return
        bullets = [
            ('بازدید و تحلیل پروژه', 'بررسی تخصصی بستر، اقلیم و نیاز سازه', 1),
            ('اجرای استاندارد', 'رعایت اصول فنی و استفاده از متریال باکیفیت', 2),
            ('پشتیبانی پس از اجرا', 'پیگیری و پاسخگویی در طول عمر پروژه', 3),
        ]
        for title, text, order in bullets:
            AboutBullet.objects.create(title=title, text=text, order=order)

    def _seed_anatomy(self):
        defaults = [
            ('فویل آلومینیوم', 'بازتاب بخش زیادی از تابش خورشید و محافظت از لایه‌های زیرین در برابر اشعه UV و فرسایش ناشی از حرارت.', '1', 1),
            ('قیر پلیمری BPP', 'هسته اصلی عایق با نقش کلیدی در آب‌بندی، مقاومت محیطی و پایداری عملکرد در شرایط مختلف آب‌وهوایی.', '2', 2),
            ('تیشو و پلی‌استر', 'تأمین استحکام کششی، افزایش مقاومت در برابر پارگی و کمک به حفظ یکپارچگی ساختار عایق.', '3', 3),
            ('لایه اتصال نهایی', 'ایجاد چسبندگی مطمئن به بستر و تکمیل فرآیند آب‌بندی با اتصال استاندارد به سطح زیرکار.', '4', 4),
        ]
        if not AnatomyLayer.objects.exists():
            for name, info_text, info_id, order in defaults:
                AnatomyLayer.objects.create(
                    name=name, info_text=info_text, info_id=info_id, order=order, depth=0
                )
            return

        for name, info_text, info_id, order in defaults:
            layer, _ = AnatomyLayer.objects.get_or_create(
                info_id=info_id,
                defaults={'name': name, 'info_text': info_text, 'order': order, 'depth': 0},
            )
            layer.name = layer.name or name
            layer.order = order
            layer.save()

    def _seed_process(self):
        if ProcessStep.objects.exists():
            return
        steps = [
            ('01', 'تماس و درخواست مشاوره', 'ثبت اطلاعات پروژه و تعیین وقت بازدید برای بررسی نیازهای عایق‌کاری', 1),
            ('02', 'بازدید و بررسی میدانی', 'ارزیابی وضعیت بنا توسط کارشناس فنی', 2),
            ('03', 'ارائه پیشنهاد فنی و مالی', 'تهیه پلان اجرایی و برآورد هزینه مکتوب', 3),
            ('04', 'انعقاد قرارداد', 'توافق شفاف با ضمانت‌نامه کتبی', 4),
            ('05', 'اجرای ایزوگام و عایق‌کاری', 'اجرای تخصصی ایزوگام توسط تیم مجرب با نظارت مستمر', 5),
            ('06', 'تحویل و پشتیبانی', 'تحویل رسمی پروژه + پشتیبانی دوره‌ای', 6),
        ]
        for step_number, title, description, order in steps:
            ProcessStep.objects.create(
                step_number=step_number, title=title, description=description, order=order
            )

    def _seed_faqs(self):
        if FAQ.objects.exists():
            return
        faqs = [
            (
                'ایزوگام برای چه فضاهایی مناسب است؟',
                'ایزوگام می‌تواند برای پشت‌بام، سرویس‌های بهداشتی، تراس، سوله و سطوحی که به عایق‌کاری رطوبتی و آب‌بندی مطمئن نیاز دارند استفاده شود؛ نوع ایزوگام و روش اجرا باید متناسب با سطح و شرایط پروژه انتخاب شود.',
                1,
            ),
            (
                'چه عواملی روی کیفیت نهایی اجرا تأثیر می‌گذارند؟',
                'کیفیت زیرسازی، تمیزی سطح، شیب مناسب، اجرای صحیح درزها، هم‌پوشانی استاندارد و تجربه تیم اجرایی از مهم‌ترین عوامل تأثیرگذار هستند.',
                2,
            ),
            (
                'آیا قبل از اجرا بازدید پروژه انجام می‌شود؟',
                'بله، برای ارائه پیشنهاد دقیق‌تر، ارزیابی بستر و تشخیص نقاط حساس پروژه، بازدید اولیه بسیار مهم است.',
                3,
            ),
            (
                'چطور می‌توانم درخواست مشاوره ثبت کنم؟',
                'کافی است فرم تماس همین صفحه را تکمیل کنید یا از طریق شماره تماس مستقیم با ما در ارتباط باشید.',
                4,
            ),
        ]
        for question, answer, order in faqs:
            FAQ.objects.create(question=question, answer=answer, order=order)
