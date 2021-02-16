from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import random

debug = True

author = "Marco Gutierrez"

doc = """
Dynamic Quiz for Understanding of a Design 
"""


class Constants(BaseConstants):
    """
    Description:
        Inherits oTree Class BaseConstants. Defines constants for
        the experiment these will remain unchanged
    """
    players_per_group = None
    players_per_group_pg = 4
    instructions_template = 'dedollarization/Instructions.html'
    contact_template = 'dedollarization/Contactenos.html'
    num_rounds = 1
    timer = 20
    payment_per_answer = c(5)

    name_in_url = 'Initial_Quiz'  # name in webbrowser

    # """Amount allocated to each player"""
    endowment = c(10)
    multiplier = 2

    '''Quiz Answers'''
    # TODO: Edit questions and answers (coded and displayed answers)

    # Answers according to the code
    quiz_fields = dict(
        question_1_response=1,
        question_2_response=3,
        question_3_response=3,
        question_4_response=0,
    )

    quiz_questions = ['q1',
                      'q2',
                      'q3',
                      'q4']

    preguntas_quiz = ['¿A qué grupo perteneces?',
                      '¿Durante el juego, en qué casos cambias de grupo?',
                      '¿En qué caso es posible intercambiar de objeto con tu socio?',
                      '¿Cuántos puntos obtendrás si decides mantener el bien de consumo durante una ronda adicional?']

    # Displayed answers
    quiz_answers = ['Rojo', 'En ningún caso cambias de grupo', 'Cuando un integrante posee un bien de consumo y '
                                                                  'el otro, una ficha', 0]
    respuestas_quiz = ['Rojo', 'En ningún caso cambias de grupo', 'Cuando un integrante posee un bien de consumo y '
                                                                  'el otro, una ficha', " '0', porque el bien de consumo "
                                                                                        "te da puntos solamente en la "
                                                                                        "ronda que lo recibes"]

    # Possible choices
    q1_choices = [[0, 'Azul'], [1, 'Rojo']]
    q1_respuestas = [[0, 'Azul'], [1, 'Rojo']]
    q2_choices = [[1, 'Cuando recibes una moneda azul de tu socio'],
                  [2, 'Cuando le entregas una moneda azul a tu socio'],
                  [3, 'En ningún caso cambias de grupo']]
    q3_choices = [[1, 'Cuando ambos tienen un bien de consumo'],
                  [2, 'Cuando ambos tienen fichas de diferentes colores'],
                  [3, 'Cuando un integrante posee un bien de consumo y el otro, una ficha']]
    q4_choices = [[0, '0'],
                  [10, '10'],
                  [50, '50']]
    # To randomize the order in which the answers are presented
    random.SystemRandom().shuffle(q1_choices)
    random.SystemRandom().shuffle(q2_choices)
    random.SystemRandom().shuffle(q3_choices)
    random.SystemRandom().shuffle(q4_choices)


class Subsession(BaseSubsession):
    """
    Description:
        Inherits oTree Class BaseSubsession. Defines subsession for
        the experiment.

    Input:
        None

    Output:
        None
    """
    def creating_session(self):
        for p in self.get_players():
            p.participant.vars['final_payoff'] = 0
            p.participant.vars['quiz_payoff'] = 0
            p.participant.vars['quiz_earnings'] = 0


class Group(BaseGroup):
    """
    Description:
        Inherits BaseGroup oTree class. Assigns group characteristics.

    Input:
        None

    Output:
        None
    """


class Player(BasePlayer):
    """
    Description:
        Inherits oTree class BasePlayer. Defines player characteristics.

    Input:
        None

    Output:
        None
    """

    time_spent_on_instructions = models.FloatField(initial=0)

    def current_field(self):
        return 'question_{}_response'.format(self.quiz_page_counter + 1)

    quiz_incorrect_answer = models.StringField(initial=None)
    quiz_respuesta_incorrecta = models.StringField(initial=None)

    # IP field
    player_ip = models.StringField()
    current_practice_page = models.IntegerField(initial=0)

    '''Quiz'''

    # Counter of the questions answered correctly on the first try
    num_correct = models.IntegerField(initial=0)
    quiz_page_counter = models.IntegerField(initial=0)
    # Inc Attemp per question
    q_incorrect_attempts = models.IntegerField(initial=0)
    q_timeout = models.IntegerField(initial=0)
    q_validation = models.IntegerField(initial=0)
    q_attempts = models.IntegerField(initial=0)
    error_sequence = models.CharField(initial='')
    timeout_sequence = models.CharField(initial='')

    question_1_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q1_respuestas)
    question_2_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q2_choices)
    question_3_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q3_choices)
    question_4_response = models.IntegerField(verbose_name='', widget=widgets.RadioSelect,
                                              choices=Constants.q4_choices)
    quiz_earnings = models.CurrencyField(initial=0)

    # For detecting bots
    quiz_dec_2 = models.LongStringField(blank=True)
