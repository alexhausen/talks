from datetime import date
from mock import Mock
from freezegun import freeze_time

from app import ListaInadimplentesUseCase

# $ source ~/.virtualenvs/venv/bin/activate
# $ python run_unit_tests.py


class DebitoRepoStub:
    def lista_debitos_por_cpfs(self, cpfs):
        return [
            {
                'id': 1,
                'cpf': '15150373044',
                'pago': False,
                'data': date(2022, 1, 1)
            }
        ]


def test_lista_cpfs_inadimplentes_stub():
    # setup
    debito_repo = DebitoRepoStub()
    # execução
    use_case = ListaInadimplentesUseCase(debito_repo)
    inadimplentes = use_case.execute(['15150373044', '21426399090'])
    # asserções
    assert inadimplentes == ['15150373044']


class DebitoRepoFake:
    fake_data = []

    def lista_debitos_por_cpfs(self, cpfs):
        return self.fake_data


def test_lista_cpfs_inadimplentes_fake():
    # setup
    debito_repo = DebitoRepoFake()
    debito_repo.fake_data = [
        {
            'id': 1,
            'cpf': '15150373044',
            'pago': False,
            'data': date(2022, 1, 1)
        }
    ]
    # execução
    use_case = ListaInadimplentesUseCase(debito_repo)
    inadimplentes = use_case.execute(['15150373044', '21426399090'])
    # asserções
    assert inadimplentes == ['15150373044']


def test_lista_cpfs_inadimplentes_mock():
    # setup
    debito_repo = Mock()
    debito_repo.lista_debitos_por_cpfs.return_value = [
        {
            'id': 1,
            'cpf': '15150373044',
            'pago': False,
            'data': date(2022, 1, 1)
        }
    ]
    # execução
    use_case = ListaInadimplentesUseCase(debito_repo)
    inadimplentes = use_case.execute(['15150373044', '21426399090'])
    # expectativas e asserções
    debito_repo.lista_debitos_por_cpfs.assert_called_with(
        ['15150373044', '21426399090'])
    assert inadimplentes == ['15150373044']


# sugestão de nome de teste:
# test_<REGRA>_deve_<RESULTADO>[_quando_CONDIÇÃO]

def test_lista_inadimplentes_deve_ser_vazia_quando_nao_possui_debitos():
    # # cobertura branch 1: condição False
    # debito_repo = Mock()
    # debito_repo.lista_debitos_por_cpfs.return_value = [
    #     {
    #         'id': 1,
    #         'cpf': '15150373044',
    #         'pago': None,
    #         'data': date(2022, 1, 1)
    #     }
    # ]
    # # execução
    # use_case = ListaInadimplentesUseCase(debito_repo)
    # inadimplentes = use_case.execute(['15150373044'])
    # # expectativas e asserções
    # debito_repo.lista_debitos_por_cpfs.assert_called_with(['15150373044'])
    # assert inadimplentes == []
    pass


def test_lista_inadimplentes_nao_deve_incluir_quem_debito_pago():
    # # cobertura branch 2: condição False
    # debito_repo = Mock()
    # debito_repo.lista_debitos_por_cpfs.return_value = [
    #     {
    #         'id': 1,
    #         'cpf': '15150373044',
    #         'pago': True,
    #         'data': date(2022, 1, 1)
    #     }
    # ]
    # # execução
    # use_case = ListaInadimplentesUseCase(debito_repo)
    # inadimplentes = use_case.execute(['15150373044'])
    # # expectativas e asserções
    # debito_repo.lista_debitos_por_cpfs.assert_called_with(['15150373044'])
    # assert inadimplentes == []
    pass


@freeze_time("2022-05-01 12:00:00")
def test_lista_inadimplentes_deve_incluir_apenas_debitos_nao_pagos_de_mais_de_30_dias():
    # # critério funcional: partição em classe de equivalência
    # debito_repo = Mock()
    # debito_repo.lista_debitos_por_cpfs.return_value = [
    #     {
    #         'id': 1,
    #         'cpf': '15150373044',
    #         'pago': False,
    #         'data': date(2022, 4, 26)  # 5 dias
    #     },
    #     {
    #         'id': 2,
    #         'cpf': '21426399090',
    #         'pago': False,
    #         'data': date(2022, 3, 1)  # 61 dias
    #     }
    # ]
    # # execução
    # use_case = ListaInadimplentesUseCase(debito_repo)
    # inadimplentes = use_case.execute(['15150373044', '21426399090'])
    # # expectativas e asserções
    # debito_repo.lista_debitos_por_cpfs.assert_called_with(
    #     ['15150373044', '21426399090'])
    # assert inadimplentes == ['21426399090']
    pass


@freeze_time("2022-05-01 12:00:00")
def test_lista_inadimplentes_deve_incluir_debitos_nao_pagos_de_30_dias_ou_mais():
    # # critério funcional: valor limite
    # debito_repo = Mock()
    # debito_repo.lista_debitos_por_cpfs.return_value = [
    #     {
    #         'id': 1,
    #         'cpf': '15150373044',
    #         'pago': False,
    #         'data': date(2022, 4, 2)  # 29 dias
    #     },
    #     {
    #         'id': 2,
    #         'cpf': '21426399090',
    #         'pago': False,
    #         'data': date(2022, 4, 1)  # 30 dias
    #     },
    #     {
    #         'id': 3,
    #         'cpf': '39328534070',
    #         'pago': False,
    #         'data': date(2022, 3, 31)  # 31 dias
    #     }
    # ]
    # # execução
    # use_case = ListaInadimplentesUseCase(debito_repo)
    # inadimplentes = use_case.execute(
    #     ['15150373044', '21426399090', '39328534070'])
    # # expectativas e asserções
    # debito_repo.lista_debitos_por_cpfs.assert_called_with(
    #     ['15150373044', '21426399090', '39328534070'])
    # assert len(inadimplentes) == 2
    # assert '21426399090' in inadimplentes
    # assert '39328534070' in inadimplentes
    pass


def test_lista_inadimplentes_cpfs_nao_encontrados():
    # # critério funcional: erros comuns (lista vazia)
    # debito_repo = Mock()
    # debito_repo.lista_debitos_por_cpfs.return_value = []
    # # execução
    # use_case = ListaInadimplentesUseCase(debito_repo)
    # inadimplentes = use_case.execute(['15150373044'])
    # # expectativas e asserções
    # debito_repo.lista_debitos_por_cpfs.assert_called_with(['15150373044'])
    # assert inadimplentes == []
    pass
