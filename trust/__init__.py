from otree.api import *

c = Currency  # old name for currency; you can delete this.


doc = """
This is a global tax competition game.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    governmentA_role = 'Government_A'
    governmentB_role = 'Government_B'
    governmentC_role = 'Government_C'
    companyA1_role = 'Company_A1'
    companyA2_role = 'Company_A2'
    companyA3_role = 'Company_A3'
    companyB1_role = 'Company_B1'
    companyB2_role = 'Company_B2'
    companyB3_role = 'Company_B3'
    companyC1_role = 'Company_C1'
    companyC2_role = 'Company_C2'
    companyC3_role = 'Company_C3'
    profit = 1000
    players_per_group = 12
    num_rounds = 3
    instructions_template = 'trust/instructions.html'


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    tax_A = models.FloatField()
    tax_B = models.FloatField()
    tax_C = models.FloatField()


class Player(BasePlayer):
    tax_rate = models.FloatField(
        min=0,
        max=100,
        label="Input 0 to 100(%):",
    )
    place = models.StringField(
        choices=[['A', 'A'], ['B', 'B'], ['C', 'C']],
        widget=widgets.RadioSelectHorizontal,
        label="choose"
    )
    tax_revenue = models.FloatField()
    profit = models.FloatField()
    location = models.StringField()

# FUNCTIONS
def tax_list(group: Group):
    tax_rates_list = {"A": 1, "B": 2, "C": 3}
    for p in group.get_players():
        if p.role == Constants.governmentA_role:
            tax_rates_list['A'] = p.tax_rate
            group.tax_A = p.tax_rate
        elif p.role == Constants.governmentB_role:
            tax_rates_list['B'] = p.tax_rate
            group.tax_B = p.tax_rate
        elif p.role == Constants.governmentC_role:
            tax_rates_list['C'] = p.tax_rate
            group.tax_C = p.tax_rate


def current_location(group: Group):
    for p in group.get_players():
        if p.role in [Constants.companyA1_role, Constants.companyA2_role, Constants.companyA3_role,
                      Constants.companyB1_role, Constants.companyB2_role, Constants.companyB3_role,
                      Constants.companyC1_role, Constants.companyC2_role, Constants.companyC3_role]:
            if group.round_number == 1:
                p.location = p.role[-2]
            else:
                p.location = p.in_round(p.round_number-1).place

def set_payoffs(group: Group):
    tax_rates_list = {"A": 1, "B": 2, "C": 3}
    for p in group.get_players():
        if p.role == Constants.governmentA_role:
            tax_rates_list['A'] = p.tax_rate
            group.tax_A = p.tax_rate
        elif p.role == Constants.governmentB_role:
            tax_rates_list['B'] = p.tax_rate
            group.tax_B = p.tax_rate
        elif p.role == Constants.governmentC_role:
            tax_rates_list['C'] = p.tax_rate
            group.tax_C = p.tax_rate

    place_list = []
    for p in group.get_players():
        if p.role in [Constants.companyA1_role, Constants.companyA2_role, Constants.companyA3_role,
                      Constants.companyB1_role, Constants.companyB2_role, Constants.companyB3_role,
                      Constants.companyC1_role, Constants.companyC2_role, Constants.companyC3_role]:
            place_list.append(p.place)

    for p in group.get_players():
        if p.role in [Constants.governmentA_role,Constants.governmentB_role,Constants.governmentC_role]:
            p.tax_revenue = p.tax_rate/100 * Constants.profit * place_list.count({Constants.governmentA_role:"A",Constants.governmentB_role:"B",Constants.governmentC_role:"C"}[p.role])
        if p. role in [Constants.companyA1_role,Constants.companyA2_role,Constants.companyA3_role,Constants.companyB1_role,Constants.companyB2_role,Constants.companyB3_role,Constants.companyC1_role,Constants.companyC2_role,Constants.companyC3_role]:
            if p.place == p.location:
                p.profit = Constants.profit * (1 - tax_rates_list[p.place] / 100)
            else:
                p.profit = Constants.profit * (1 - tax_rates_list[p.place] / 100 - 0.02)




# PAGES
class Introduction(Page):
    pass


class Tax(Page):

    form_model = 'player'
    form_fields = ['tax_rate']

    @staticmethod
    def is_displayed(player: Player):
        print("current players role is: "+ player.role)
        return player.role == Constants.governmentA_role or player.role == Constants.governmentB_role or player.role == Constants.governmentC_role

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        if group.round_number == 1:
            tax_a_old = 20
            tax_b_old = 20
            tax_c_old = 20
        else:
            tax_a_old = group.in_round(group.round_number-1).tax_A
            tax_b_old = group.in_round(group.round_number-1).tax_B
            tax_c_old = group.in_round(group.round_number-1).tax_C

        return dict(tax_a_old = tax_a_old, tax_b_old = tax_b_old, tax_c_old = tax_c_old)



class MultiWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        tax_rates_list = {"A": 1, "B": 2, "C": 3}
        for p in group.get_players():
            if p.role == Constants.governmentA_role:
                tax_rates_list['A'] = p.tax_rate
                group.tax_A = p.tax_rate
            elif p.role == Constants.governmentB_role:
                tax_rates_list['B'] = p.tax_rate
                group.tax_B = p.tax_rate
            elif p.role == Constants.governmentC_role:
                tax_rates_list['C'] = p.tax_rate
                group.tax_C = p.tax_rate

        for p in group.get_players():
            if p.role in [Constants.companyA1_role, Constants.companyA2_role, Constants.companyA3_role,
                          Constants.companyB1_role, Constants.companyB2_role, Constants.companyB3_role,
                          Constants.companyC1_role, Constants.companyC2_role, Constants.companyC3_role]:
                if group.round_number == 1:
                    p.location = p.role[-2]
                else:
                    p.location = p.in_round(p.round_number - 1).place


class Response(Page):

    form_model = 'player'
    form_fields = ['place']

    @staticmethod
    def is_displayed(player: Player):
        return player.role != Constants.governmentA_role and player.role != Constants.governmentB_role and player.role != Constants.governmentC_role

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(tax_a = group.tax_A, tax_b = group.tax_B, tax_c = group.tax_C)

class LastWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass

page_sequence = [
    Introduction,
    Tax,
    MultiWaitPage,
    Response,
    LastWaitPage,
    Results,
]
