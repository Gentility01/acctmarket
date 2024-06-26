from django.db.models import IntegerChoices, TextChoices


class ProductStatus(TextChoices):
    PROCESSING = ("PROCESSING", "PROCESSING")
    SHIPPED = ("SHIPPED", "SHIPPED")
    DELIVERD = ("DELIVERD", "DELIVERD")


class Status(TextChoices):
    DRAFT = ("DRAFT", "DRAFT")
    DISABLED = ("DISABLED", "DISABLED")
    IN_REVIEW = ("IN_REVIEW", "IN_REVIEW")
    REJECTED = ("REJECTED", "REJECTED")
    PUBLISHED = ("PUBLISHED", "PUBLISHED")


class Rating(IntegerChoices):
    ONE_STAR = 1, "⭐"
    TWO_STARS = 2, "⭐⭐"
    THREE_STARS = 3, "⭐⭐⭐"
    FOUR_STARS = 4, "⭐⭐⭐⭐"
    FIVE_STARS = 5, "⭐⭐⭐⭐⭐"


class Ticket(TextChoices):
    OPEN = ("OPEN", "OPEN")
    IN_PROGRESS = ("IN_PROGRESS", "IN_PROGRESS")
    CLOSED = ("CLOSED", "CLOSED")
