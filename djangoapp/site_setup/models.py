from django.db import models
from utils import model_validators, image

class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)
    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)
    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True,
        default='',
        validators=[model_validators.validate_png]
    )

    def save(self, *agrs, **kwargs):
        current_favicon_name = str(self.favicon.name)
        # print(current_favicon_name)
        super().save(*agrs, **kwargs)
        favicon_changed = False
        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon
        
        if favicon_changed:
            image.resize_image(self.favicon, 32)

    def __str__(self):
        return self.title
class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    def __str__(self):
        return self.text