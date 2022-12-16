from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class AuditModel(models.Model):
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = fields.UUIDField(pk=True)

    class Meta:
        abstract = True


class Company(UUIDModel, AuditModel):
    name = fields.CharField(max_length=150)

    def __str__(self):
        return self.name


class JobOffer(UUIDModel, AuditModel):
    name = fields.CharField(max_length=150)
    currency = fields.CharField(max_length=15)
    salary = fields.IntField()
    url = fields.TextField()
    company = fields.ForeignKeyField(
        "models.Company", related_name="job_offers"
    )

    def __str__(self):
        return self.name


class User(UUIDModel, AuditModel):
    first_name = fields.CharField(max_length=150)
    last_name = fields.CharField(max_length=150)
    email = fields.CharField(max_length=255)
    years_of_experience = fields.IntField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Skill(UUIDModel, AuditModel):
    name = fields.CharField(max_length=150)

    def __str__(self):
        return self.name


class UserSkill(UUIDModel, AuditModel):
    user = fields.ForeignKeyField(
        "models.User", related_name="skills"
    )
    skill = fields.ForeignKeyField(
        "models.Skill", related_name="users"
    )
    years_of_experience = fields.IntField()

    def __str__(self):
        return f"{self.user} {self.skill}"


class JobOfferSkill(UUIDModel, AuditModel):
    job_offer = fields.ForeignKeyField(
        "models.JobOffer", related_name="skills"
    )
    skill = fields.ForeignKeyField(
        "models.Skill", related_name="job_offers"
    )
    years_of_experience = fields.IntField()

    def __str__(self):
        return f"{self.job_offer} {self.skill}"


SkillSchema = pydantic_model_creator(Skill)
CompanySchema = pydantic_model_creator(Company)
JobOfferSchema = pydantic_model_creator(JobOffer)
JobOfferSkillSchema = pydantic_model_creator(JobOfferSkill)
UserSchema = pydantic_model_creator(User)
UserSkillSchema = pydantic_model_creator(UserSkill)
