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
    companyA1_role = 'Company_A1'
    companyA2_role = 'Company_A2'
    companyA3_role = 'Company_A3'
    companyB_role = 'Company_B'
    companyC_role = 'Company_C'
    
    players_per_group = 12
    num_rounds = 1
    instructions_template = 'trust/instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    tax_rate = models.FloatField(
        min=0,
        max=100,
        label="Input 0 to 100(%):",
    )
    place = models.StringField(label="""Input A,B, or C""")



class Player(BasePlayer):
    pass


# FUNCTIONS

# def creating_session(subsession):
#     if subsession.round_number == 1:
#     else:
#         subsession.group_like_round(1)
#     print("####s started!!!!")
#     for p in player.get_players():
#         if p.id_in_group % 4 == 0:
#             p.participant.vars['role'] = Constants.government_role
#         elif p.id_in_group %4 == 1:
#             p.participant.vars['role']=Constants.companyA_role
#         elif p.id_in_group %4 == 2:
#             p.participant.vars['role']=Constants.companyB_role
#         elif p.id_in_group %4 == 3:
#             p.participant.vars['role']=Constants.companyC_role
#
#         print("role assigned to"+p.participant.vars['role'])
#         p.type=p.participant.vars['role']


def sent_back_amount_max(group: Group):
    return group.place


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = 1 
    p2.payoff = 2


# PAGES
class Introduction(Page):
    #print("Introduction Page started!!!")
    pass

class Tax(Page):


    form_model = 'group'
    form_fields = ['tax_rate']

    @staticmethod
    def is_displayed(player: Player):
        print("current players role is: "+ player.role)
        return player.role == Constants.governmentA_role_role or player.role = Constants.gover


class SendBackWaitPage(WaitPage):
    pass


class Response(Page):
    """This page is only for P2
    P2 sends back some amount (of the tripled amount received) to P1"""

    form_model = 'group'
    form_fields = ['place']

    @staticmethod
    def is_displayed(player: Player):
        print("current players role is: "+ player.role)
        return player.role == Constants.agent_role

    @staticmethod
    def vars_for_template(player: Player):
        

        tripled_amount = 1
        return dict(tripled_amount=tripled_amount)


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    """This page displays the earnings of each player"""

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        profit = 1000
        return dict(profit=profit)

page_sequence = [
    Introduction,
    Tax,
    SendBackWaitPage,
    Response,
    ResultsWaitPage,
    Results,
]
