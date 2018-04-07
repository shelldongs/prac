# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin


class BaseOwnerAdmin(object):
    def get_list_queryset(self):
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        if self.request.user.is_superuser:
            return qs
        return qs.filter(owner=self.request.user)

    def save_models(self):
        if not self.org_obj:
            self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()
