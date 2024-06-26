import auto_prefetch
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from acctmarket.utils.models import UIDTimeBasedModel

from .managers import UserManager


class User(UIDTimeBasedModel, AbstractUser):
    """
    Default custom user model for Acctmarket.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name: str = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email: str = EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]
    phone_no: str = CharField(_("Phone number"), max_length=20, default="", blank=True)
    country: str = CountryField(_("Country"), blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's Details.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.email

    @property
    def is_customer_support_representative(self):
        return CustomerSupportRepresentative.objects.filter(user=self).exists()

    @property
    def is_content_manager(self):
        return ContentManager.objects.filter(user=self).exists()

    @property
    def is_customer(self):
        return Customer.objects.filter(user=self).exists()


class Account(UIDTimeBasedModel):
    owner = auto_prefetch.ForeignKey(
        User,
        related_name="owned_accounts",
        on_delete=models.CASCADE,
        verbose_name=_("Account Owner"),
    )

    class Meta(UIDTimeBasedModel.Meta):
        verbose_name_plural = "Accounts"


class BaseProfile(UIDTimeBasedModel):
    """
    Base class for different types of profiles associated with users.
    """

    user = auto_prefetch.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_profiles",
        verbose_name=_("User"),
    )
    account = auto_prefetch.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        verbose_name=_("Account"),
        related_name="%(class)s_profiles",
    )

    class Meta(UIDTimeBasedModel.Meta):
        abstract = True


class Customer(BaseProfile):
    """
    represent a customer
    """

    def __str__(self):
        return self.user.name


class Administrator(BaseProfile):
    """
    Represents an administrator associated with an account.
    """

    department = models.CharField(_("Department"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Administrators"


class CustomerSupportRepresentative(BaseProfile):
    """
    Represents a customer support representative associated with an account.
    """

    department = models.CharField(_("Department"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Customer Support Representatives"

    def save(self, *args, **kwargs):
        if not self.department:
            self.department = (
                "General"  # Set default value if department is not provided
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.name


class ContentManager(BaseProfile):
    """
    Represents a content manager associated with an account.
    """

    expertise_area = models.CharField(_("Expertise Area"), max_length=255)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Content Managers"

    def save(self, *args, **kwargs):
        if not self.expertise_area:
            self.expertise_area = (
                "General"  # Set default value if expertise_area is not provided
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class MarketingAndSales(BaseProfile):
    """
    Represents a marketing and sales personnel associated with an account.
    """

    marketing_strategy = models.TextField(_("Marketing Strategy"))

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Marketing and Sales"

    def save(self, *args, **kwargs):
        if not self.marketing_strategy:
            self.marketing_strategy = (
                "Perfect"  # Set default value if expertise_area is not provided
            )
        super().save(*args, **kwargs)


class Accountant(BaseProfile):
    """
    Represents an accountant associated with an account.
    """

    financial_software_used = models.CharField(
        _("Financial Software Used"),
        max_length=100,
    )

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Accountants"

    def save(self, *args, **kwargs):
        if not self.financial_software_used:
            self.financial_software_used = "Real One"
        super().save(*args, **kwargs)


class HelpDeskTechnicalSupport(BaseProfile):
    """
    Represents a technical support personnel associated with an account.
    """

    technical_skills = models.TextField(_("Technical Skills"))

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Help Desk Technical Supports"

    def save(self, *args, **kwargs):
        if not self.technical_skills:
            self.technical_skills = "Web dev"
        super().save(*args, **kwargs)


class LiveChatSupport(BaseProfile):
    """
    Represents a live chat support personnel associated with an account.
    """

    languages_spoken = models.CharField(_("Languages Spoken"), max_length=100)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Live Chat Supports"

    def save(self, *args, **kwargs):
        if not self.languages_spoken:
            self.languages_spoken = "English"
        super().save(*args, **kwargs)


class AffiliatePartner(BaseProfile):
    """
    Represents an affiliate partner associated with an account.
    """

    affiliate_code = models.CharField(_("Affiliate Code"), max_length=20)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Affiliate Partners"

    def save(self, *args, **kwargs):
        if not self.affiliate_code:
            self.affiliate_code = "412"
        super().save(*args, **kwargs)


class DigitalGoodsDistribution(BaseProfile):
    """
    Represents digital goods distribution associated with an account.
    """

    delivery_method = models.CharField(_("Delivery Method"), max_length=50)

    class Meta(BaseProfile.Meta):
        verbose_name_plural = "Digital Goods Distributions"

    def save(self, *args, **kwargs):
        if not self.delivery_method:
            self.delivery_method = "Fast"
        super().save(*args, **kwargs)
