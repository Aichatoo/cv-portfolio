from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.documents.models import Document
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    """Page d'accueil du portfolio"""
    
    # Hero Section
    hero_title_fr = models.CharField(
        max_length=255,
        default="Développeuse Web & Spécialiste Customer Success",
        verbose_name="Titre Hero (FR)"
    )
    hero_title_en = models.CharField(
        max_length=255,
        default="Web Developer & Customer Success Specialist",
        verbose_name="Titre Hero (EN)"
    )
    hero_subtitle_fr = models.CharField(
        max_length=100,
        default="Bilingue Français | Anglais",
        verbose_name="Sous-titre (FR)"
    )
    hero_subtitle_en = models.CharField(
        max_length=100,
        default="Bilingual French | English",
        verbose_name="Sous-titre (EN)"
    )
    hero_description_fr = RichTextField(
        blank=True,
        verbose_name="Description Hero (FR)"
    )
    hero_description_en = RichTextField(
        blank=True,
        verbose_name="Description Hero (EN)"
    )
    
    # About Section
    about_title_fr = models.CharField(
        max_length=100,
        default="À propos",
        verbose_name="Titre About (FR)"
    )
    about_title_en = models.CharField(
        max_length=100,
        default="About Me",
        verbose_name="Titre About (EN)"
    )
    about_text_fr = RichTextField(
        blank=True,
        verbose_name="Texte About (FR)"
    )
    about_text_en = RichTextField(
        blank=True,
        verbose_name="Texte About (EN)"
    )
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # CV PDF
    cv_document_fr = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="CV PDF Français"
    )
    cv_document_en = models.ForeignKey(
        'wagtaildocs.Document',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="CV PDF English"
    )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title_fr'),
            FieldPanel('hero_title_en'),
            FieldPanel('hero_subtitle_fr'),
            FieldPanel('hero_subtitle_en'),
            FieldPanel('hero_description_fr'),
            FieldPanel('hero_description_en'),
        ], heading="Section Hero"),
        
        MultiFieldPanel([
            FieldPanel('about_title_fr'),
            FieldPanel('about_title_en'),
            FieldPanel('about_text_fr'),
            FieldPanel('about_text_en'),
        ], heading="Section À propos"),
        
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone'),
            FieldPanel('location'),
            FieldPanel('linkedin_url'),
            FieldPanel('github_url'),
            FieldPanel('cv_document_fr'),
            FieldPanel('cv_document_en'),
        ], heading="Contact"),
        
        InlinePanel('skills', label="Compétences"),
        InlinePanel('experiences', label="Expériences"),
        InlinePanel('projects', label="Projets"),
        InlinePanel('education', label="Formation"),
    ]
    
    max_count = 1
    
    class Meta:
        verbose_name = "Page d'accueil"


class Skill(models.Model):
    """Modèle pour les compétences"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=50,
        choices=[
            ('webdev', 'Développement Web'),
            ('customer', 'Customer Success'),
            ('digital', 'Marketing Digital'),
            ('tools', 'Outils & CRM'),
        ]
    )
    level = models.IntegerField(
        default=50,
        help_text="Niveau de compétence (0-100)"
    )
    order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
        FieldPanel('level'),
        FieldPanel('order'),
    ]
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"


class Experience(models.Model):
    """Modèle pour les expériences professionnelles"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='experiences')
    year = models.CharField(max_length=20, help_text="Ex: 2022 ou 2020-2021")
    title_fr = models.CharField(max_length=200, verbose_name="Titre (FR)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (EN)")
    company = models.CharField(max_length=200)
    description_fr = RichTextField(blank=True, verbose_name="Description (FR)")
    description_en = RichTextField(blank=True, verbose_name="Description (EN)")
    order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('year'),
        FieldPanel('title_fr'),
        FieldPanel('title_en'),
        FieldPanel('company'),
        FieldPanel('description_fr'),
        FieldPanel('description_en'),
        FieldPanel('order'),
    ]
    
    class Meta:
        ordering = ['-order']
        verbose_name = "Expérience"
        verbose_name_plural = "Expériences"


class Project(models.Model):
    """Modèle pour les projets"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='projects')
    title_fr = models.CharField(max_length=200, verbose_name="Titre (FR)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (EN)")
    description_fr = RichTextField(verbose_name="Description (FR)")
    description_en = RichTextField(verbose_name="Description (EN)")
    technologies = models.CharField(
        max_length=300,
        help_text="Séparées par des virgules (ex: Python, Django, Wagtail)"
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('title_fr'),
        FieldPanel('title_en'),
        FieldPanel('description_fr'),
        FieldPanel('description_en'),
        FieldPanel('technologies'),
        FieldPanel('github_url'),
        FieldPanel('live_url'),
        FieldPanel('order'),
    ]
    
    class Meta:
        ordering = ['order']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"


class Education(models.Model):
    """Modèle pour la formation"""
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='education')
    year = models.CharField(max_length=20)
    title_fr = models.CharField(max_length=200, verbose_name="Titre (FR)")
    title_en = models.CharField(max_length=200, verbose_name="Titre (EN)")
    institution = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    panels = [
        FieldPanel('year'),
        FieldPanel('title_fr'),
        FieldPanel('title_en'),
        FieldPanel('institution'),
        FieldPanel('description'),
        FieldPanel('order'),
    ]
    
    class Meta:
        ordering = ['-order']
        verbose_name = "Formation"
        verbose_name_plural = "Formations"