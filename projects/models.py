# -----------------------------------------------------------------------------
#    Karajlug.org
#    Copyright (C) 2010  Karajlug community
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# -----------------------------------------------------------------------------

from django.db import models
from django.utils.translation import ugettext as _


class Project(models.Model):
    """
    Project main model
    """
    LANGUAGES = [
        ["0", "en-us"],
        ["1", "fa"],
    ]

    VCS = [
        ("0", "Git"),
        ("1", "Mercurial"),
        ("2", "SVN"),
        ]
    language = models.CharField(choices=LANGUAGES,
                            default="0",
                            max_length=1,
                            verbose_name=_("Language"),
                            help_text=_("Site language (en-us at this time)"))

    name = models.CharField(max_length=64,
                            verbose_name=_("Project Name"))
    version = models.CharField(max_length=16,
                               blank=True,
                               null=True,
                               verbose_name=_("Version"))
    slug = models.SlugField(verbose_name=_("Slug"),
                            unique=True)

    maintainers = models.ManyToManyField("auth.User",
                                related_name="%(app_label)s_%(class)s_related",
                                verbose_name=_("Maintainers"))

    logo = models.ImageField(blank=True, null=True,
                    upload_to="uploads/logos/",
                    verbose_name=_("Project logo"),
                    help_text=_("Size: 128x128 DO NOT UPLOAD BIG FILES !!!"))

    license = models.CharField(verbose_name=_("License"),
                               max_length=16,
                               blank=True, null=True)
    home = models.URLField(verbose_name=_("Home Page"),
                           verify_exists=False,
                           blank=True, null=True)
    vcs = models.CharField(max_length=1,
                           choices=VCS,
                           blank=True, null=True,
                           verbose_name=_("VCS"))
    downloadlink = models.URLField(verbose_name=_("Download URL"),
                                   verify_exists=False,
                                   blank=True, null=True)
    creator = models.ForeignKey("auth.User", verbose_name=_("Creator"),
                             editable=False)

    weight = models.IntegerField(default=40, verbose_name=_("Order"),
                help_text=_("Projects will appear in menu respect to this value"))

    kproject = models.BooleanField(default=False,
                                   verbose_name=_("KarajLUG Project"))
    desc = models.TextField(verbose_name=_("Description"),
                            blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/projects/%s/" % self.slug

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class Repository(models.Model):
    """
    Repository model.
    """
    project = models.ForeignKey(Project,
                                verbose_name=_("Project"))
    address = models.CharField(max_length=265,
                               verbose_name=_("Address"))

    weight = models.IntegerField(default=40, verbose_name=_("Order"),
        help_text=_("Repository will appear in menu respect to this value"))

    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name = _("Repository")
        verbose_name_plural = _("Reporsitories")