from otree.api import *

c = Currency  # old name for currency; you can delete this.


doc = """
This is a global tax competition game.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    government_role = 'Government'
    companyA_role = 'Company_A'
    companyB_role = 'Company_B'
    companyC_role = 'Company_C'
    players_per_group = 12
    num_rounds = 1
    instructions_template = 'trust/instructions.html'


class Subsession(BaseSubsession):
    def role(subsession):
        subsession.group_randomly(fixed_id_in_group=True)
        for p in subsession.get_players():
            if p.id_in_group % 4 == 0:
                p.participant.vars['role']='government'
            elif p.id_in_group %4 == 1:
                p.participant.vars['role']='company_A'
            elif p.id_in_group %4 == 2:
                p.participant.vars['role']='company_B'
            elif p.id_in_group %4 == 3:
                p.participant.vars['role']='company_C'
            p.type=p.participant.vars['role']


class Group(BaseGroup):
    tax_rate = models.FloatField(
        min=0,
        max=100,
        label="Input 0 to 100(%):",
    )
    place = models.StringField(label="""Input A,B, or C""")


class Player(BasePlayer):
    def role(player):
        if player.
    pass


def set_payoffs(group: Group):
    Gov = group.get_player_by_role(Constants.government_role)
    A = group.get_player_by_role(Constants.companyA_role)
    B = group.get_player_by_role(Constants.companyB_role)
    C = group.get_player_by_role(Constants.companyC_role)
    Gov.payoff = group.tax_rate*1000
    A.payoff=1000*(1-group.tax_rate)
    B.payoff=1000*(1-group.tax_rate)
    C.payoff=1000*(1-group.tax_rate)


# PAGES
class Introduction(Page):
    pass


class Tax(Page):


    form_model = 'group'
    form_fields = ['tax_rate']

    @staticmethod
    def is_displayed(player: Player):
        return player.role == Constants.government_role


class SendBackWaitPage(WaitPage):
    pass


class Response(Page):


    form_model = 'group'
    form_fields = ['place']

    @staticmethod
    def is_displayed(player: Player):
        return player.role != Constants.government_role

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        tax_rate_A=
        tax_rate_B=
        tax_rate_C=
        profit = 1000 *(1-group.tax_rate)
        return dict(profit=profit)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return 3


page_sequence = [
    Introduction,
    Tax,
    SendBackWaitPage,
    Response,
    ResultsWaitPage,
    Results,
]
