from django.db import models
from django.utils.text import slugify

class CourseCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Course(models.Model):
    LEVEL_CHOICES = (
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name="courses")
    thumbnail = models.ImageField(upload_to="courses/")
    short_description = models.CharField(max_length=500)
    long_description = models.TextField()
    features = models.TextField(
        help_text="Enter features separated by commas, e.g., Feature1, Feature2, Feature3"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Optional discounted price"
    )

    duration = models.CharField(max_length=100, help_text="e.g. 6 Months, 3 Months")
    total_lessons = models.PositiveIntegerField(default=0)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    rating = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_feature_list(self):
        return [f.strip() for f in self.features.split(",") if f.strip()]

    def get_display_price(self):
        if self.discount_price:
            return f"${self.discount_price} (was ${self.price})"
        return f"${self.price}"


# -----------------------------
# Course Reviews Model
# -----------------------------
class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=100)
    rating = models.FloatField(default=5.0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Review"
        verbose_name_plural = "Course Reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.course.title}"
