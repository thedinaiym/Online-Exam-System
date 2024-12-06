from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class question(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    qno = models.IntegerField()
    question = models.CharField(max_length=100)
    o1 = models.CharField(max_length=100)
    o2 = models.CharField(max_length=100)
    o3 = models.CharField(max_length=100)
    o4 = models.CharField(max_length=100)
    co = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.subject.name} - {self.question}"

class leaderboard(models.Model):
    username = models.CharField(max_length=100)
    # Add a default subject or make the field nullable
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, null=True)  # Make it nullable
    # OR
    # subject = models.ForeignKey('Subject', on_delete=models.CASCADE, default=your_default_subject_id)
    score = models.IntegerField()
    
    def __str__(self):
        return f"{self.username} - {self.subject.name if self.subject else 'No Subject'}"

class fraud_model(models.Model):
    username = models.CharField(max_length=100)
    fraud = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
