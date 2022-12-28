import sys

from app import DebitoRepository
from app import ListaInadimplentesUseCase

# source ~/.virtualenvs/venv/bin/activate
# python run_app.py 729.192.590-83


def run(cpfs):
    repo = DebitoRepository()
    use_case = ListaInadimplentesUseCase(repo)
    inadimplentes = use_case.execute(cpfs)
    print(str(inadimplentes))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Wrong number of arguments')
        exit(1)
    run(sys.argv[1:])
