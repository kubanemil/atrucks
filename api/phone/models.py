from django.db import models


class PhoneInfo(models.Model):
    abc_code = models.IntegerField()
    min_code = models.IntegerField()
    max_code = models.IntegerField()
    operator = models.TextField()
    region = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["abc_code", "min_code", "max_code"], name="unique_phone_info"
            )
        ]

    def __str__(self):
        return f"{self.abc_code} {self.min_code}-{self.max_code}"
