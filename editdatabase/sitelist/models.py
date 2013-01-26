from django.db import models

# Create your models here.

class Site(models.Model):
	name = models.CharField(max_length=30) 
	chrom = models.CharField(max_length=10)
	position = models.CharField(max_length=20)
	gene = models.CharField(max_length=20)
	strand = models.CharField(max_length=1)
	annot1 = models.CharField(max_length=20)
	annot2 = models.CharField(max_length=20)
	alu = models.CharField(max_length=3)
	repnonalu = models.CharField(max_length=3)
	ref = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Mouse(models.Model):
	name = models.CharField(max_length=30) 
	chrom = models.CharField(max_length=10)
	position = models.CharField(max_length=20)
	gene = models.CharField(max_length=20)
	strand = models.CharField(max_length=1)
	annot1 = models.CharField(max_length=20)
	annot2 = models.CharField(max_length=20)
	alu = models.CharField(max_length=3)
	repnonalu = models.CharField(max_length=3)
	ref = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

class Fly(models.Model):
	name = models.CharField(max_length=30) 
	chrom = models.CharField(max_length=10)
	position = models.CharField(max_length=20)
	gene = models.CharField(max_length=20)
	strand = models.CharField(max_length=1)
	annot1 = models.CharField(max_length=20)
	annot2 = models.CharField(max_length=20)
	alu = models.CharField(max_length=3)
	repnonalu = models.CharField(max_length=3)
	ref = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name	
