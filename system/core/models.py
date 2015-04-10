#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import logging 

from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import signals
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal
from PIL import Image as Img
from sorl.thumbnail import ImageField

logger = logging.getLogger(__name__)

def validate_image(value): 
	if not (value.name.lower().endswith('.jpg') or value.name.lower().endswith('.jpeg') \
		or value.name.lower().endswith('.png') or value.name.lower().endswith('.bmp') \
		or  value.name.lower().endswith('.gif')):
		raise ValidationError('Unsupported format. Please use .jpg, .jpeg, .png, .bmp or .gif.')	
		
def validate_audio(value):
	if not (value.name.lower().endswith('.mp3') or value.name.lower().endswith('.wav') or value.name.lower().endswith('.ogg')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .mp3, .wav ou .ogg.')	
		
def validate_video(value):
	if not (value.name.lower().endswith('.mp4') or value.name.lower().endswith('.webm') or value.name.lower().endswith('.ogg')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .mp4, .webm ou .ogg.')	
	
def validate_document(value):
	if not (value.name.lower().endswith('.pdf')):
		raise ValidationError(u'Formato não suportado. Por favor, envie um arquivo no formato .pdf.')
	
def create_resized_images(sender, instance):
	conf = {
		'small': {
			'w': 300, 'h': 180
		}, 
		'medium': {
			'w': 570, 'h': 320
		}, 
		'big': {
			'w': 1200, 'h': 675
		},
	}
	default_color = (255, 255, 255, 0)
	photo_path = unicode(instance.photo.path)
	photo = Image.open(photo_path) 
	extension = photo_path.rsplit('.', 1)[1]
	file_name = photo_path.rsplit("/",1)[1].rsplit(".")[0]
	directory = photo_path.rsplit('/', 1)[0]
	
	if photo.mode not in ("L", "RGB"):
		photo = photo.convert("RGB")

	if extension not in ['jpg', 'jpeg', 'gif', 'png']: 
		sys.exit()
	
	photo.thumbnail((conf['big']['w'], conf['big']['h']), Image.ANTIALIAS)
	
	big = Image.new("RGBA", (conf['big']['w'], conf['big']['h']), default_color)
	big.paste(photo, ((conf['big']['w'] - photo.size[0]) / 2, (conf['big']['h'] - photo.size[1]) / 2))
	big.save(os.path.join(directory, file_name + "-big.png"), 'PNG', quality=100)
	
	photo.thumbnail((conf['medium']['w'], conf['medium']['h']), Image.ANTIALIAS)
	
	medium = Image.new("RGBA", (conf['medium']['w'], conf['medium']['h']), default_color)
	medium.paste(photo, ((conf['medium']['w'] - photo.size[0]) / 2, (conf['medium']['h'] - photo.size[1]) / 2))
	medium.save(os.path.join(directory, file_name + "-medium.png"), 'PNG', quality=100)
	
	photo.thumbnail((conf['small']['w'], conf['small']['h']), Image.ANTIALIAS)
	
	small = Image.new("RGBA", (conf['small']['w'], conf['small']['h']), default_color)
	small.paste(photo, ((conf['small']['w'] - photo.size[0]) / 2, (conf['small']['h'] - photo.size[1]) / 2))
	small.save(os.path.join(directory, file_name + "-small.png"), 'PNG', quality=100)

def clear_images(image):
	image_path = unicode(image.path)
	filename = image_path.rsplit('/', 1)[1].rsplit('.')[0]
	directory = image_path.rsplit('/', 1)[0]
	
	try:
		os.remove(photo_path)
	except Exception, e:
		logger.warning(str(e))
	try:
		os.remove(os.path.join(directory, filename + '-big.png'))
	except Exception, e:
		logger.warning(str(e))
	try:
		os.remove(os.path.join(directory, filename + '-medium.png'))
	except Exception, e:
		logger.warning(str(e))
	try:
		os.remove(os.path.join(directory, filename + '-small.png'))
	except Exception, e:
		logger.warning(str(e))

class Category(models.Model):
	'''
	Categoria
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Category name'))
		
	class Meta:
		verbose_name = _('Category')
		verbose_name_plural = _('Categories')
	
	def __unicode__(self):
		return '%s' % self.name

class OriginalSource(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Original source name'))
		
	class Meta:
		verbose_name = _('Original source')
		verbose_name_plural = _('Original sources')
	
	def __unicode__(self):
		return '%s' % self.name

class Function(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Function name'))
		
	class Meta:
		verbose_name = _('Function')
		verbose_name_plural = _('Functions')
	
	def __unicode__(self):
		return '%s' % self.name		

class Author(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Author name'))
	artistic_name = models.CharField(_('Artistic name'), max_length=128, unique=True, help_text=_('Author artistic name'))
	function = models.ForeignKey(Function, verbose_name=_('Function'), null=True, help_text=_('Author function'))
		
	class Meta:
		verbose_name = _('Author')
		verbose_name_plural = _('Authors')
	
	def __unicode__(self):	
		result = self.name

		if self.artistic_name:
			retorno += ' (%s) ' % self.artistic_name

		if self.function:
			retorno += ' - %s' % self.function.name
		
		return result

class Source(models.Model):
	'''
	Procedência
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Source name'))
		
	class Meta:
		verbose_name = _('Source')
		verbose_name_plural = _('Sources')
	
	def __unicode__(self):
		return '%s' % self.name

class Origin(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Origin name'))
		
	class Meta:
		verbose_name = _('Origin')
		verbose_name_plural = _('Origins')
	
	def __unicode__(self):
		return '%s' % self.name

class Owner(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Owner name'))
		
	class Meta:
		verbose_name = _('Owner')
		verbose_name_plural = _('Owners')
	
	def __unicode__(self):
		return '%s' % self.name

class FormerOwner(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Former owner name'))
		
	class Meta:
		verbose_name = _('Former owner')
		verbose_name_plural = _('Former owners')
	
	def __unicode__(self):
		return '%s' % self.name	

class Section(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Section name'))
		
	class Meta:
		verbose_name = _('Section')
		verbose_name_plural = _('Sections')
	
	def __unicode__(self):
		return '%s' % self.name
	
class Collection(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Collection name'))
		
	class Meta:
		verbose_name = _('Collection')
		verbose_name_plural = _('Collections')
	
	def __unicode__(self):
		return '%s' % self.name	

class Subcollection(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Sub collection name'))
	collection = models.ForeignKey(Collection, verbose_name=_('Collection'), help_text=_('Sub collection collection'))
		
	class Meta:
		verbose_name = _('Sub collection')
		verbose_name_plural = _('Sub collections')
	
	def __unicode__(self):
		return '%s' % self.name	

class Material(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Material name'))
		
	class Meta:
		verbose_name = _('Material')
		verbose_name_plural = _('Materials')
	
	def __unicode__(self):
		return '%s' % self.name	
		
class Tecnique(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Tecnique name'))
		
	class Meta:
		verbose_name = _('Tecnique')
		verbose_name_plural = _('Tecniques')
	
	def __unicode__(self):
		return '%s' % self.name	

class Acquisition(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Acquisition name'))
		
	class Meta:
		verbose_name = _('Acquisition')
		verbose_name_plural = _('Acquisitions')
	
	def __unicode__(self):
		return '%s' % self.name	
		
class Provisor(models.Model):
	'''
	Provisor
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Provisor name'))
		
	class Meta:
		verbose_name = _('Provisor')
		verbose_name_plural = _('Provisors')
	
	def __unicode__(self):
		return '%s' % self.name	

class Role(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Role name'))
		
	class Meta:
		verbose_name = _('Role')
		verbose_name_plural = _('Roles')
	
	def __unicode__(self):
		return '%s' % self.name	

class Team(models.Model):
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Team name'))
		
	class Meta:
		verbose_name = _('Team')
		verbose_name_plural = _('Teams')
	
	def __unicode__(self):
		return '%s' % self.name	
			
class Object(models.Model):
	'''
	Object
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Object name'))
		
	class Meta:
		verbose_name = _('Object')
		verbose_name_plural = _('Objects')
	
	def __unicode__(self):
		return '%s' % self.name	

class CurrencyType(models.Model):
	'''
	Tipo da moeda
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Currency type name'))
		
	class Meta:
		verbose_name = _('Currency type')
		verbose_name_plural = _('Currency types')
	
	def __unicode__(self):
		return '%s' % self.name	

class FormattedDate(models.Model):
	date = models.DateField(_('Date'), blank=True, null=True, help_text=_('Date DD/MM/YYYY'))
	decade = models.CharField(_('Decade'), blank=True, null=True, max_length=4, help_text=_('Decade'))
	seculo = models.CharField(_('Seculo'), blank=True, null=True, max_length=3, help_text=_('Seculo'))
	period = models.CharField(_('Period'), blank=True, null=True, max_length=50, help_text=_('Period'))

	class Meta:
		verbose_name = _('Date')
		verbose_name_plural = _('Dates')
	
	def __unicode__(self):
		date = None

		if self.date:
			date = self.date.strftime('%d/%m/%Y')
		elif self.decade:
			date = '%s %s' % (_('Decade of'), self.decade)
		elif self.seculo:
			date = '%s %s' % (_('Seculo of'), self.seculo)
		elif self.period:
			date = '%s %s' % (_('Period of'), self.period)

		return date

class Part(models.Model):
	'''
	Peça
	'''
	register = models.CharField(_('Register'), unique=True, max_length=32, help_text=_('Part register'))
	
	section = models.ForeignKey(Section, verbose_name=_('Section'), blank=True, null=True, help_text=_('Part section'))
	collection = models.ForeignKey(Collection, verbose_name=_('Collection'), blank=True, null=True, help_text=_('Part collection'))
	subcollection =  models.ForeignKey(Subcollection, verbose_name=_('Sub collection'), blank=True, null=True, help_text=_('Part subcollection'))

	obj = models.ForeignKey(Object, verbose_name=_('Object'), help_text=_('Part object type'))
	authors = models.ManyToManyField(Author, verbose_name=_('Authors'), help_text=_('Part authors'))
	creation_date = models.ForeignKey(FormattedDate, verbose_name=_('Creation date'), related_name='creation', help_text=_('Part creation date'))
	category = models.ForeignKey(Category, verbose_name=_('Category'), blank=True, null=True, help_text=_('Part category'))
	
	title = models.CharField(_('Title'), max_length=128, help_text=_('Part title'))
	description = models.TextField(_('Description'), max_length=512, help_text=_('Part description'))

	iconography = models.TextField(_('Iconography'), max_length=512, blank=True, help_text=_('Part iconography'))
	observations = models.TextField(_('Observations'), max_length=512, blank=True, help_text=_('Part observations'))
	historical_date = models.TextField(_('Historical date'), max_length=512, blank=True, help_text=_('Part historical date'))
	reference = models.TextField(_('Reference'), max_length=512, blank=True, help_text=_('Part reference'))
	text = models.TextField(_('Text'), max_length=512, blank=True, help_text=_('Part text'))
	
	origin = models.ForeignKey(Origin, verbose_name=_('Origin'), blank=True, null=True, help_text=_('Part origin'))
	source = models.ForeignKey(Source, verbose_name=_('Source'), blank=True, null=True, help_text=_('Part source'))
	owner = models.ForeignKey(Owner, verbose_name=_('Owner'), blank=True, null=True, help_text=_('Part owner'))
	
	acquisition_method = models.ForeignKey(Acquisition, verbose_name=_('Acquisition method'), blank=True, null=True, help_text=_('Part acquisition method'))
	acquisition_date = models.ForeignKey(FormattedDate, verbose_name=_('Acquisition date'), blank=True, null=True, related_name='acquisition', help_text=_('Part acquisition date'))
	
	process_number = models.CharField(_('Process number'), max_length=128, blank=True, null=True, help_text=_('Part process number'))
	
	provisor = models.ForeignKey(Provisor, verbose_name=_('Provisor'), blank=True, null=True, help_text=_('Part provisor'))
	
	currency_type = models.ForeignKey(CurrencyType, verbose_name=_('Currency type'), blank=True, null=True, help_text=_('Part currency type'))
	acquisition_value = models.DecimalField(_('Acquisition value'), max_digits=10, default=Decimal('0.00'), decimal_places=2, blank=True, null=True, help_text=_('Part acquisition value'))
	insurance_value = models.DecimalField(_('insurance value'), max_digits=10, default=Decimal('0.00'), decimal_places=2, blank=True, null=True, help_text=_('Part insurance value'))
	
	former_owner = models.ForeignKey(FormerOwner, verbose_name=_('Former owner'), blank=True, null=True, help_text=_('Part former owner'))
	
	original_source = models.ForeignKey(OriginalSource, verbose_name=_('Original source'), blank=True, null=True, help_text=_('Original source'))

	number_of_pieces = models.IntegerField(_('Number of pieces'), blank=True, null=True, help_text=_('Part number of pieces'))

	material = models.ForeignKey(Material, verbose_name=_('Material'), blank=True, null=True)
	tecnique = models.ForeignKey(Tecnique, verbose_name=_('Tecnique'), blank=True, null=True)

	height = models.FloatField(_('Height'), blank=True, null=True)	
	
	circumference = models.FloatField(_('Circumference'), blank=True, null=True)

	diameter = models.FloatField(_('Diameter'), blank=True, null=True)	
	length = models.FloatField(_('Length'), blank=True, null=True)	
	width = models.FloatField(_('Width'), blank=True, null=True)	
	weight = models.FloatField(_('Weight'), blank=True, null=True)	
	depth = models.FloatField(_('Depth'), blank=True, null=True)	

	keywords = models.CharField(_('Keywords'), max_length=128, blank=True, null=True, help_text=_('Part keywords'))

	functionary = models.ForeignKey(User, editable=False, verbose_name=_('Functionary'), blank=True, null=True)
	create_date = models.DateField(auto_now=True)
	
	class Meta:
		verbose_name = _('Part')
		verbose_name_plural = _('Parts')

	def __unicode__(self):
		return '%s' % self.titulo
	
	def image(self):
		return Image.objects.filter(part=self)
	
	def video(self):
		return Video.objects.filter(part=self)
	
	def audio(self):
		return Audio.objects.filter(part=self)
	
	def doc(self):
		return Documento.objects.filter(part=self)

	def report_generate(self):
		return '<a href=%s>Gerar Relatório</a>' % ('/gerenciamento/relatorio/%d/' % (self.pk))

	report_generate.allow_tags = True	

class Image(models.Model):
	part = models.ForeignKey(Part)
	author = models.ForeignKey(Author, verbose_name=_('Author'), blank=True, null=True, help_text=_('Image author'))
	date = models.DateField(_('Date'), blank=True, null=True, help_text=_('Image date'))

	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_PART_IMAGE_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			name = hash_code + '.png'
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					name = hash_code + '.png'
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	image = ImageField(upload_to=create_path, max_length=256, validators=[validate_image], help_text=_('Image'))

	class Meta:
		verbose_name = _('Image')
		verbose_name_plural = _('Images')

	def __unicode__(self):
		return '%s' % (self.pk)

	def small(self):
		extension = self.image.url.rsplit('.', 1)[1]
		image_name = self.image.url.rsplit('fotec', 1)[1]
		return image_name.replace('.' + extension, '-small.png')

	def medium(self):
		extension = self.image.url.rsplit('.', 1)[1]
		image_name = self.image.url.rsplit('fotec', 1)[1]
		return image_name.replace('.' + extension, '-medium.png')

	def big(self):
		extension = self.image.url.rsplit('.', 1)[1]
		image_name = self.image.url.rsplit('fotec', 1)[1]
		return image_name.replace('.' + extension, '-big.png')

	def image_tag(self):
		return '<img src="%s"/>' % (self.small())

	image_tag.short_description = _('Current image')
	image_tag.allow_tags = True

@receiver(signals.pre_save, sender=Image)
def image_pre_save(sender, instance, **kwargs):
	try:
		image = Image.objects.get(pk=instance.pk).image
	except Exception, e:
		logger.info(str(e))
	else:
		if image != instance.image:
			clear_images(image)

@receiver(signals.post_save, sender=Image)
def image_post_save(sender, instance, **kwargs):
	create_resized_images(sender, instance)

@receiver(signals.pre_delete, sender=Image)
def image_pre_delete(sender, instance, **kwargs):		
	clear_images(instance.image)
	
class Audio(models.Model):
	part = models.ForeignKey(Part)
	author = models.ForeignKey(Author, verbose_name=_('Author'), blank=True, null=True, help_text=_('Audio author'))
	date = models.DateField(_('Date'), blank=True, null=True, help_text=_('Audio date'))

	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_PART_AUDIO_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			extension = filename.split('.')[1]
			name = hash_code + '.' + extension
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					extension = filename.split('.')[1]
					name = hash_code + '.' + extension
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	audio = models.FileField(upload_to=create_path, max_length=256, blank=True, validators=[validate_audio], help_text=_('Audio'))

	class Meta:
		verbose_name = _('Audio')
		verbose_name_plural = _('Audios')

	def __unicode__(self):
		return '%s' % (self.pk)	
	
@receiver(signals.pre_save, sender=Audio)
def audio_pre_save(sender, instance, **kwargs):
	try:
		audio = Audio.objects.get(id=instance.id).audio
	except Exception, e:
		logger.info(str(e))
	else:
		if audio != instance.audio:
			try:
				os.remove(audio.path)
			except Exception, e:
				logger.error(str(e))

@receiver(signals.pre_delete, sender=Audio)
def audio_pre_delete(sender, instance, **kwargs):
	try:
		os.remove(instance.audio.path)
	except Exception, e:
		logger.error(str(e))

class Video(models.Model):
	part = models.ForeignKey(Part)
	author = models.ForeignKey(Author, verbose_name=_('Author'), blank=True, null=True, help_text=_('Video author'))
	date = models.DateField(_('Date'), blank=True, null=True, help_text=_('Video date'))
	
	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_PART_VIDEO_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			extension = filename.split('.')[1]
			name = hash_code + '.' + extension
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					extension = filename.split('.')[1]
					name = hash_code + '.' + extension
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	video = models.FileField(upload_to=create_path, max_length=256, blank=True, validators=[validate_video], help_text=_('Video'))

	class Meta:
		verbose_name = _('Video')
		verbose_name_plural = _('Videos')

	def __unicode__(self):
		return '%s' % (self.pk)	

@receiver(signals.pre_save, sender=Video)
def video_pre_save(sender, instance, **kwargs):
	try:
		video = Video.objects.get(id=instance.id).video
	except Exception, e:
		logger.info(str(e))
	else:
		if video != instance.video:
			try:
				os.remove(video.path)
			except Exception, e:
				logger.error(str(e))

@receiver(signals.pre_delete, sender=Video)
def video_pre_delete(sender, instance, **kwargs):
	try:
		os.remove(instance.video.path)
	except Exception, e:
		logger.error(str(e))
	
class OtherNumber(models.Model):
	part = models.ForeignKey(Part)
	number = models.CharField(_('Number'), max_length=16, help_text=_('Other number number'))
	observation = models.CharField(_('Observation'), max_length=128, help_text=_('Other number observation'))
			
	class Meta:
		verbose_name = _('Other number')
		verbose_name_plural = _('Others numbers')

	def __unicode__(self):
		return '%s' % sself.numero

class Document(models.Model):
	part = models.ForeignKey(Part)
	author = models.ForeignKey(Author, verbose_name=_('Author'), blank=True, null=True, help_text=_('Document author'))
	date = models.DateField(_('Date'), blank=True, null=True, help_text=_('Document date'))
	
	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_PART_DOCUMENT_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			extension = filename.split('.')[1]
			name = hash_code + '.' + extension
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					extension = filename.split('.')[1]
					name = hash_code + '.' + extension
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	video = models.FileField(upload_to=create_path, max_length=256, blank=True, validators=[validate_document], help_text=_('Document'))

	class Meta:
		verbose_name = _('Document')
		verbose_name_plural = _('Documents')

	def __unicode__(self):
		return '%s' % (self.pk)	

@receiver(signals.pre_save, sender=Document)
def document_pre_save(sender, instance, **kwargs):
	try:
		document = Document.objects.get(id=instance.id).document
	except Exception, e:
		logger.info(str(e))
	else:
		if document != instance.document:
			try:
				os.remove(document.path)
			except Exception, e:
				logger.error(str(e))

@receiver(signals.pre_delete, sender=Document)
def document_pre_delete(sender, instance, **kwargs):
	try:
		os.remove(instance.document.path)
	except Exception, e:
		logger.error(str(e))
	
class Preservation(models.Model):
	'''
	Estado de conservação
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Preservation name'))
		
	class Meta:
		verbose_name = _('Preservation')
		verbose_name_plural = _('Preservations')
	
	def __unicode__(self):
		return '%s' % self.name		

class PreservationHistoric(models.Model):
	part = models.ForeignKey(Part)
	avaliation_date = models.DateTimeField(_('Avaliation date'), blank=True, null=True)
	preservation = models.ForeignKey(Preservation, verbose_name=_('Preservation'), blank=True, null=True)
	description = models.TextField(_('Description'), max_length=128, blank=True, null=True)
	functionary = models.ForeignKey(User, verbose_name=_('Functionary'), blank=True, null=True)

	class Meta:
		unique_together = ('part','avaliation_date')
		verbose_name = _('Preservation historic')
		verbose_name_plural = _('Preservation historics')
	
	def __unicode__(self): 
		return '%s' % self.part.title.lower()
	
class Intervention(models.Model):
	part = models.ForeignKey(Part)
	intervention_date = models.DateTimeField(_('Intervention date'), blank=True, null=True)
	description = models.TextField(_('Description'), max_length=128, blank=True, null=True)
	functionary = models.ForeignKey(User, verbose_name=_('Functionary'), blank=True, null=True)

	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_INTERVENTION_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			name = hash_code + '.png'
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					name = hash_code + '.png'
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	image = ImageField(upload_to=create_path, max_length=256, validators=[validate_image], help_text=_('Image'))
	
	class Meta:
		unique_together = ('part','intervention_date')
		verbose_name = _('Intervention')
		verbose_name_plural = _('Interventions')

	def __unicode__(self):
		return '%s' % self.part.title.lower()
		
@receiver(signals.pre_save, sender=Intervention)
def image_pre_save(sender, instance, **kwargs):
	try:
		image = Intervention.objects.get(pk=instance.pk).image
	except Exception, e:
		logger.info(str(e))
	else:
		if image != instance.image:
			clear_images(image)

@receiver(signals.post_save, sender=Intervention)
def image_post_save(sender, instance, **kwargs):
	create_resized_images(sender, instance)

@receiver(signals.pre_delete, sender=Intervention)
def image_pre_delete(sender, instance, **kwargs):		
	clear_images(instance.image)
	
class Locality(models.Model):
	'''
	Localidade
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Locality name'))
		
	class Meta:
		verbose_name = _('Locality')
		verbose_name_plural = _('Localities')
	
	def __unicode__(self):
		return '%s' % self.name		
		
class MovimentationHistoric(models.Model):
	part = models.ForeignKey(Part)
	movimentation_date = models.DateTimeField(_('Avaliation date'), blank=True, null=True)
	description = models.TextField(_('Description'), max_length=128, blank=True, null=True)
	fixed_location = models.ForeignKey(Locality, verbose_name=_('Fixed location'), blank=True, null=True, related_name='fixed')
	current_location = models.ForeignKey(Locality, verbose_name=_('Current location'), blank=True, null=True, related_name='current')
		
	class Meta:
		unique_together = ('part','movimentation_date')
		verbose_name = _('Movimentation historic')
		verbose_name_plural = _('Movimentation historics')

	def __unicode__(self):
		return '%s' % self.part.title.lower()
		
class SubscriptionType(models.Model):
	'''
	Tipo de inscrição
	'''
	name = models.CharField(_('Name'), max_length=128, unique=True, help_text=_('Subscription type name'))
		
	class Meta:
		verbose_name = _('Subscription type')
		verbose_name_plural = _('Subscription types')
	
	def __unicode__(self):
		return '%s' % self.name		

class Subscription(models.Model):
	part = models.ForeignKey(Part)
	movimentation_date = models.DateTimeField(_('Avaliation date'), blank=True, null=True)
	signed_part = models.BooleanField(_('Sined part'), blank=True)
	description = models.TextField(_('Description'), max_length=128, blank=True, null=True)
	subscription_type = models.ForeignKey(SubscriptionType, verbose_name=_('Subscription type'), blank=True, null=True, related_name='type')
	signature_locality = models.ForeignKey(Locality, verbose_name=_('Signature locality'), blank=True, null=True, related_name='signature')
		
	def create_path(self, filename):
		try:
			folder_path = os.path.join(settings.MEDIA_SUBSCRIPTION_ROOT, unicode(self.part.pk))
			hash_code = uuid.uuid4().hex 
			name = hash_code + '.png'
			
			try:
				list = os.listdir(folder_path)
			except Exception, e:
				logger.error(str(e))
			else:
				while True:
					if not name in list:
						break

					hash_code = uuid.uuid4().hex 
					name = hash_code + '.png'
			finally:
				return os.path.join(folder_path, name)
		except Exception, e:
			logger.error(str(e))

	image = ImageField(upload_to=create_path, max_length=256, validators=[validate_image], help_text=_('Image'))
	
	class Meta:
		verbose_name = _('Subscription')
		verbose_name_plural = _('Subscriptions')

	def __unicode__(self):
		return '%s' % self.part.title.lower()
	
@receiver(signals.pre_save, sender=Subscription)
def image_pre_save(sender, instance, **kwargs):
	try:
		image = Subscription.objects.get(pk=instance.pk).image
	except Exception, e:
		logger.info(str(e))
	else:
		if image != instance.image:
			clear_images(image)

@receiver(signals.post_save, sender=Subscription)
def image_post_save(sender, instance, **kwargs):
	create_resized_images(sender, instance)

@receiver(signals.pre_delete, sender=Subscription)
def image_pre_delete(sender, instance, **kwargs):		
	clear_images(instance.image)
	
class InformacoesIPHAN(models.Model):
	part = models.ForeignKey(Part)
	memory_and_history = models.TextField(_('Memory and history'), max_length=128, blank=True, null=True)
	knowledge_and_practices = models.TextField(_('Knowledge and practices'), max_length=128, blank=True, null=True)
	celebrations = models.TextField(_('Celebrations'), max_length=128, blank=True, null=True)
	places = models.TextField(_('Places'), max_length=128, blank=True, null=True)
	expressions = models.TextField(_('Expressions'), max_length=128, blank=True, null=True)

	class Meta:
		verbose_name = _('IPHAN information')
		verbose_name_plural = _('IPHAN informations')
	
	def __unicode__(self):
		return '%s' % self.pk