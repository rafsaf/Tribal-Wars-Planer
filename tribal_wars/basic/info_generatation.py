from django.utils.translation import gettext as _

from base import models
from tribal_wars import basic


class OutlineInfo:
    def __init__(self, outline: models.Outline):
        """
        Generate basic informations about outline like targets cord
        and players nicks.
        """
        self.outline = outline
        self.real_targets = basic.TargetWeightQueries(outline=outline).targets
        self.all_targets = basic.TargetWeightQueries(
            outline=outline, every=True
        ).target_dict_with_weights_read()
        self.target_message = _("Targets:") + "\r\n"
        self.fake_message = _("Fakes:") + "\r\n"
        self.players = ""
        self.world_evidence = basic.world_evidence(self.outline.world)

    def generate_nicks(self):
        result = _("Nicknames: ") + "\r\n\r\n"
        targets_ids = [target.id for target in self.all_targets]

        unique_weights = (
            models.WeightModel.objects.filter(target__in=targets_ids)
            .order_by("player")
            .distinct("player")
        )
        counter = 1
        for weight in unique_weights:
            if counter == 50:
                counter = 0
                result += "\r\n\r\n"
            counter += 1
            result += f"{weight.player};"
        self.players = result

    def generate_sum_up(self):
        for target, lst in self.all_targets.items():
            if target in self.real_targets:
                self.generete_real_target(target, lst)
            else:
                self.generete_fake_target(target, lst)

    def generete_fake_target(self, target, lst):
        only_offs = len([weight for weight in lst if weight.nobleman == 0])
        only_nobles = len([weight for weight in lst if weight.nobleman > 0])
        fakes = _("fakes")
        nobles = _("fake nobles")
        self.fake_message += (
            f"{target.target} - {only_offs} {fakes} - {only_nobles} {nobles}\r\n"
        )

    def generete_real_target(self, target, lst):
        only_offs = len([weight for weight in lst if weight.nobleman == 0])
        only_nobles = len([weight for weight in lst if weight.nobleman > 0])
        offs = _("offs")
        nobles = _("nobles")
        self.target_message += (
            f"{target.target} - {only_offs} {offs} - {only_nobles} {nobles}\r\n"
        )

    def show_sum_up(self):
        self.generate_sum_up()
        return self.target_message + "\r\n\r\n" + self.fake_message

    def parse_weight_to_army(self, weight_max: models.WeightMaximum, line_lst, noble_index):
        line_lst[0] = str(weight_max.start) + ","
        line_lst[3] = str(weight_max.off_left) + ","
        line_lst[noble_index] = str(weight_max.nobleman_left) + ","
        return "".join(line_lst)

    def show_export_troops(self):
        evidence_dictionary = {
            (1, 1, 1): 16,
            (1, 1, 0): 15,
            (0, 1, 1): 15,
            (1, 0, 1): 14,
            (1, 0, 0): 13,
            (0, 0, 1): 13,
            (0, 1, 0): 14,
            (0, 0, 0): 12,
        }
        line_length = evidence_dictionary[self.world_evidence]
        line_lst = ["0," for i in range(line_length)]
        if self.world_evidence[1] == 0:
            if self.world_evidence[0] == 0:
                noble_index = 9
            else:
                noble_index = 10
        elif self.world_evidence[0] == 0:
            noble_index = 11
        else:
            noble_index = 12
        
        sum_text = ""
        for weight_max in models.WeightMaximum.objects.filter(outline=self.outline):
            sum_text += self.parse_weight_to_army(weight_max, line_lst, noble_index)
            sum_text += "\r\n"
        return sum_text

