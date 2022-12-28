from datetime import date
from .debito_model import Debito


class ListaInadimplentesUseCase:
    def __init__(self, debito_repo):
        self.debito_repo = debito_repo

    def execute(self, cpfs):
        rows = self.debito_repo.lista_debitos_por_cpfs(cpfs)
        inadimplentes = set()
        for row in rows:
            if row['data'] and row['pago'] is not None:  # 1
                debito = Debito(row['data'], row['pago'])
                dias_em_debito = date.today() - debito.data
                if not debito.pago and dias_em_debito.days > 30:  # 2
                    inadimplentes.add(row['cpf'])
        return list(inadimplentes)
