from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField()
    importance = models.IntegerField()
    dependencies = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return self.title


# ---------- ADD THIS BELOW TASK MODEL ----------
class ScoringConfig(models.Model):
    urgency = models.FloatField(default=1.5)
    importance = models.FloatField(default=2.0)
    effort = models.FloatField(default=1.2)
    dependencies = models.FloatField(default=1.8)
    last_updated = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "urgency": self.urgency,
            "importance": self.importance,
            "effort": self.effort,
            "dependencies": self.dependencies,
        }

    def __str__(self):
        return f"ScoringConfig({self.urgency}, {self.importance}, {self.effort}, {self.dependencies})"
