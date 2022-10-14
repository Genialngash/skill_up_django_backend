from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class AccessPackage(models.Model):
    image = ProcessedImageField(
        upload_to="media/payments/products/photos/%Y/",
        processors=[Thumbnail(425, 490)],
        format="JPEG",
        options={"quality": 100},
        default="default.jpg",
    )
    title = models.CharField(max_length=128)
    unlocks = models.IntegerField(null=False, default=False)
    price = models.PositiveIntegerField()
    stripe_product_id = models.CharField(max_length=96, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=96, blank=True, null=True)
    expires_in = models.IntegerField(null=False, blank=False)
    job_cards = models.PositiveIntegerField(null=False, blank=False)
    description = models.TextField()
    tag = models.CharField(max_length=36, default='unlock_code_package')

    def __str__(self):
        return self.title
 
    class Meta:
        ordering = ['-id']
        verbose_name = 'Unlocks Package'
        verbose_name_plural = 'Unlocks Packages'
