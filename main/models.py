from django.db import models

# Team member model
class TeamMember(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='team_members/')

    def __str__(self):
        return self.name


# Service model
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name


# Service features (for ✅ Customized solution etc.)
class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.service.name} - {self.feature}"


# Client reviews
class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=150)
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.service.name}"
