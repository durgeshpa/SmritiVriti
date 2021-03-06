from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core import validators
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

#from .managers import CustomUserManager


class UserManager(BaseUserManager):
	def _create_user(self, email_or_phone, password,is_staff, is_superuser, **extra_fields):
		""" Create EmailPhoneUser with the given email or phone and password.

		:param str email_or_phone: user email or phone
		:param str password: user password
		:param bool is_staff: whether user staff or not
		:param bool is_superuser: whether user admin or not

		:return settings.AUTH_USER_MODEL user: user
		:raise ValueError: email or phone is not set
		:raise NumberParseException: phone does not have correct format

		"""
		if not email_or_phone:
			raise ValueError('The given email_or_phone must be set')

		if "@" in email_or_phone:
			email_or_phone = self.normalize_email(email_or_phone)
			username, email, phone = (email_or_phone, email_or_phone, "")
		else:
			email_or_phone = self.normalize_email(email_or_phone) 
			username, email, phone = (email_or_phone, "", email_or_phone)

		now = timezone.now()
		is_active = extra_fields.pop("is_active", True)
		user = self.model(
			username=username,
			email=email,
			mobile_no=phone,
			is_staff=is_staff,
			is_active=is_active,
			is_superuser=is_superuser,
			#last_login=now,
			date_joined=now,
			**extra_fields
		)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_user(self, email_or_phone, password=None, **extra_fields):
		return self._create_user(email_or_phone, password, False, False,**extra_fields)

	def create_superuser(self, username, password, **extra_fields):
		"""
		Create and save a SuperUser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		user = self.model(username=username, **extra_fields)
		user.set_password(password)
		user.save()
		return user
		#return self.create_user(email, password, **extra_fields)



	#def create_superuser(self, email_or_phone, password, **extra_fields):
		#return self._create_user(email_or_phone, password, True, True,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(
		_('user_name'), max_length=255, unique=True, db_index=True,
		help_text=_('Required. 255 characters or fewer. Letters, digits and '
					'@/./+/-/_ only.'),
		validators=[validators.RegexValidator(
			r'^[\w.@+-]+$', _(
				'Enter a valid username. '
				'This value may contain only letters, numbers '
				'and @/./+/-/_ characters.'
			), 'invalid'),
		],
		error_messages={
			'unique': _("A user with that username already exists."),
		})
	email = models.EmailField(
		verbose_name = _('email address'), max_length = 255, blank = True
	)
	mobile_no = models.CharField(_('mobile_no'),max_length=25,blank=True)
	# password field supplied by AbstractBaseUser
	# last_login field supplied by AbstractBaseUser


	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_(
			'Designates whether the user can log into this admin site.'
		),
	)
	# is_superuser field provided by PermissionsMixin
	# groups field provided by PermissionsMixin
	# user_permissions field provided by PermissionsMixin

	date_joined = models.DateTimeField(
		_('date joined'), default=timezone.now
	)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	class Meta:
		permissions  =(('can upload mp3','for provide mp3'),
			          ("can_listion mp3", "only user can listen"),)
	#REQUIRED_FIELDS = []
	#AUTH_USER_MODE

	'''class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')
		abstract = True'''

	def get_full_name(self):
		""" Return the full name for the user."""
		return self.username

	def get_short_name(self):
		""" Return the short name for the user."""
		return self.username

	def email_user(self, subject, message, from_email=None, **kwargs):
		""" Send an email to this User."""
		send_mail(subject, message, from_email, [self.email], **kwargs)


'''class EmailPhoneUser(User):

	""" Concrete class of AbstractEmailPhoneUser.

	Use this if you don't need to extend EmailPhoneUser.

	"""

	class Meta(User.Meta):
		swappable = 'AUTH_USER_MODEL'''
