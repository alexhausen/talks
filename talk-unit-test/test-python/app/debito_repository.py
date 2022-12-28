from datetime import date


class DebitoRepository:
    def lista_debitos_por_cpfs(self, cpfs):
        # SELECT * FROM debito WHERE cpf IN cpfs
        tabela_debito = [
            {
                'id': 1,
                'cpf': '15150373044',
                'pago': None,
                'data': None
            },
            {
                'id': 2,
                'cpf': '21426399090',
                'pago': True,
                'data': date(2022, 1, 1)
            },
            {
                'id': 3,
                'cpf': '39328534070',
                'pago': True,
                'data': date.today()
            },
            {
                'id': 4,
                'cpf': '39328534070',
                'pago': False,
                'data': date.today()
            },
            {
                'id': 5,
                'cpf': '41513558048',
                'pago': False,
                'data': date(2022, 1, 1)
            },
            {
                'id': 6,
                'cpf': '57991403033',
                'pago': True,
                'data': date(2022, 1, 1)
            },
            {
                'id': 7,
                'cpf': '57991403033',
                'pago': False,
                'data': date(2022, 1, 1)
            },
        ]
        return list(filter(lambda row: row['cpf'] in cpfs, tabela_debito))
