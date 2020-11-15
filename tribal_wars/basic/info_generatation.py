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
        self.target_message = "Cele:\r\n"
        self.fake_message = "Fejki:\r\n"
        self.players = ""

    def generate_nicks(self):
        result = "Nicki: \r\n\r\n"
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
        self.fake_message += (
            f"{target.target} - {only_offs} fejków - {only_nobles} grubych\r\n"
        )

    def generete_real_target(self, target, lst):
        only_offs = len([weight for weight in lst if weight.nobleman == 0])
        only_nobles = len([weight for weight in lst if weight.nobleman > 0])
        self.target_message += (
            f"{target.target} - {only_offs} offów - {only_nobles} grubych\r\n"
        )

    def show_sum_up(self):
        self.generate_sum_up()
        return self.target_message + "\r\n\r\n" + self.fake_message
