from django.db import models


class Permalinkable(models.Model):

    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def get_url_kwargs(self, **kwargs):
        kwargs.update(getattr(self, "url_kwargs", {}))
        return kwargs

    def get_absolute_url(self):
        url_kwargs = self.get_url_kwargs(slug=self.slug)
        url_name = getattr(self, "url_name", "")
        return url_name, (), url_kwargs

    def pre_save(self, instance, add):
        from django.utils.text import slugify

        if not instance.slug:
            slug_source = getattr(self, "slug_source")
            if not slug_source:
                self.slug_source = getattr(self, "title")
            instance.slug = slugify(self.slug_source)
