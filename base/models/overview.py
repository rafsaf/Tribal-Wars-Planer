# Copyright 2021 Rafał Safin (rafsaf). All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from typing import TYPE_CHECKING

from django.db import models
from django.http import HttpRequest
from django.urls import reverse

if TYPE_CHECKING:
    from base.models import Outline


class Overview(models.Model):
    """Present results for tribe members using unique urls"""

    outline_overview = models.ForeignKey("OutlineOverview", on_delete=models.CASCADE)
    token = models.CharField(max_length=100, primary_key=True, db_index=True)
    outline = models.ForeignKey(
        "Outline", on_delete=models.SET_NULL, null=True, blank=True
    )
    player = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    table = models.TextField()
    string = models.TextField()
    extended = models.TextField(default="")
    deputy = models.TextField(default="")
    show_hidden = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)

    def get_absolute_url(self):
        return reverse("base:overview", args=[self.token])

    def extend_with_encodeURIComponent(
        self, instance: "Outline", request: HttpRequest
    ) -> None:
        from utils.basic import encode_component

        setattr(self, "to", encode_component(self.player))

        message: str = f"[b]{self.player}[/b]\n\n"
        f2 = f"[url]{request.scheme}://{request.get_host()}{self.get_absolute_url()}[/url]\n\n"

        if instance.sending_option == "string":
            message += instance.text_message + self.string
        elif instance.sending_option == "extended":
            message += instance.text_message + self.extended
        elif instance.sending_option == "deputy":
            message += instance.text_message + self.deputy
        else:
            message += f2 + instance.text_message

        setattr(
            self,
            "message",
            encode_component(message.replace("[size=12]", "").replace("[/size]", "")),
        )