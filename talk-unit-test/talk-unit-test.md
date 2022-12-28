---
marp: true
footer: "3778.care"
paginate: true
theme: default
style: |
  h1 {
    color: white;
  }
  blockquote {
    color: lightgreen;
  }
  section {
    background-color: black;
    color: lightgray;
  }
  a {
    color: lightgreen;
  }
  code {
    display: inline-block;
    background-color: white;
    color: black;
  }
---

# Tech-Talk Testes Unitários

<br>

> _How I Learned to Stop Worrying and Love Tests_

<br>
<br>

## :warning: Atenção, as definições apresentadas podem variar de acordo com o autor

## alexandre.hausen@3778.care

<style scoped>
h2 {
  font-size: 18px;
}
</style>
<!-- _paginate: false -->

---

# Agenda

![bg right:60%](img/agenda.jpg)

- Introdução e conceitos
- Q&As _vs._ _devs_?
- \+ Conceitos
  - unidade
  - _stub_, _fake_ e _mock_
- Exemplos
- \++ Conceitos
  - critérios
  - aplicação dos critérios

---

# No início era o caos

- sem ferramentas de código (_eg_ linters/formatadores/analisadores estáticos)
- sem controle de versão
- sem testes automatizados

<br>

E portanto sem [CI](https://en.wikipedia.org/wiki/Continuous_integration), muito menos [CD](https://en.wikipedia.org/wiki/Continuous_deployment).

---

# O tempo passa, as pessoas aprendem (as vezes)

- ferramentas de código integradas às IDEs/CLI

- Git é padrão de fato

---

# E o teste?

## Pra que serve?

> Encontrar defeitos. :bug:

A gente só corrige os defeitos que conhece.

<br>

## Pra que não serve?

> Para dizer que o sistema **não** tem defeitos.

Pode ser que os testes **ainda** não tenham encontrado defeitos.

---

# O que é teste?

:books: É a análise dos **artefatos** e **comportamentos** do software através dos processos de **verificação** e **validação**.

## E na prática?

1. verificação: "Nós construímos corretamente o software?" (_ie_ ele implementa os requisitos)
2. validação: "Nós construímos o software correto?" (_ie_ ele atende às expectativas do cliente)

---

# Como verificamos e validamos?

Da mesma forma, respondendo a pergunta:

> Para uma dada entrada, a saída obtida é igual a saída esperada?

---

# Quem diz o que é o esperado?

- pessoa: especialista, analista de negócio, cliente, _product owner_, ...

- documento: requisitos, _user stories_, regras de negócio, diagramas, leis, normas, ...

---

# Por que o desenvolvedor testa se temos Q&A?

Porque os propósitos são diferentes e complementares.

---

## Testes de sistema (Q&A)

O objetivo é encontrar defeitos (funcionais e não-funcionais) no sistema usando testes manuais e ferramentas de automação.
<br>
Mas sempre com uma versão completa do sistema (_release_, _pre-release_, prd, dev ou local).

---

## Testes unitários (desenvolvedor)

O objetivo é encontrar defeitos (funcionais) nas unidades.

E também:

- orienta o desenvolvimento unidades novas
- auxilia a correção de _bugs_
- evita regressão (_ie_ que o _bug_ volte a ocorrer)
- dá confiança para realizar melhorias (_aka refactoring_)
- executado automaticamente (ambientes local e CI)

---

## O que é uma unidade?

É a menor parte do software a qual podemos verificar uma funcionalidade.

Em geral: uma função, um método, uma classe.

<br>

![image height:350](img/lego-castle.jpg) ![image height:350](img/lego-brick.jpg)

---

> _User story:_ Como um Analista de Cobrança, gostaria de saber quais pessoas de uma lista estão inadimplentes\*, para emitir cobranças.
>
> \* débito não pago há 30 dias ou mais.

---

```python
"""Caso de uso para listar pessoas inadimplentes"""
class Debito:
    def __init__(self, data, pago):
        self.data = data
        self.pago = pago

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
```

```
Executar exemplo python
# source ~/.virtualenvs/venv/bin/activate
# python run_app.py 15150373044 21426399090 39328534070 41513558048 57991403033
```

---

> _Requisito funcional:_ O sistema deve alertar o usuário ao digitar um CPF inválido.

---

```typescript
function isValidCPF(cpf: string): boolean {
  cpf = cpf.replace(/\D/g, "");
  if (cpf.length !== 11) return false;
  const cpfDigits: number[] = cpf.split("").map((item) => +item);
  const rest = (count: number) =>
    ((cpfDigits
      .slice(0, count - 12)
      .reduce((soma, item, index) => soma + item * (count - index), 0) *
      10) %
      11) %
    10;
  return rest(10) === cpfDigits[9] && rest(11) === cpfDigits[10];
}
```

Inspirado em [gist.github.com](https://gist.github.com/joaohcrangel/8bd48bcc40b9db63bef7201143303937?permalink_comment_id=3781326)

```
Executar exemplo typescript
# npx ts-node ./src/index.ts 729.192.590-83
```

---

# Como testar a unidade?

Isolando-a do resto do sistema, substituindo as dependências e testando diferentes cenários de maneira determinística.

---

## E o que é uma dependência (no contexto de teste unitário)?

É tudo que você precisa configurar antes de executar o objeto do teste, _ie_ aquilo que se quer testar (_System Under Test_ ou SUT).
A dependência pode ser:

1. explícita: valores passados como entrada para o SUT (_eg_ construtor, método ou função chamada)
2. implícita: instâncias construídas dentro do SUT e as fontes de não-determinismo

---

## Precisa isolar completamente para ser teste unitário?

:see_no_evil:

Vale o bom senso, quanto mais isolado melhor você consegue controlar o teste da unidade, porém o _setup_ das dependências será mais complicado.

---

## Como substituir as dependências?

1. Inversão de dependência
   - Substituindo a instância passada por parâmetro
   - Substituindo o criador da instância (_eg_ [_factory_](https://en.wikipedia.org/wiki/Factory_method_pattern))
2. Sobrescrever o objeto/classe
   - [_monkey patching_](https://en.wikipedia.org/wiki/Monkey_patch) + [_duck typing_](https://en.wikipedia.org/wiki/Duck_typing)
   - _interface_/classe abstrata
3. Facilidades do _framework_/linguagem

---

## Substituir pelo quê?

![bg vertical right:40%](img/candle_stub.jpg)
![bg](img/fake.jpg)
![bg](img/alfred_neuman_3usd.jpg)

Por algo que eu possa controlar o comportamento.

- _stub_
- _fake_
- _mock_

---

### Qual é a diferença entre _stub_, _fake_ e _mock_?

- _stub_: uma implemantação vazia (ou fixa) da dependência

- _fake_: um objeto com implementação simplificada (_eg_ pseudo banco em memória)

- _mock_: um objeto/função com comportamento controlado (_ie_ controle das expectativas de como deve ser chamado, dos valores de retorno e as exceções lançadas)

---

## Quais são os passos para testar uma unidade?

![bg](img/dogs.jpeg)
![](#000)

1. _setup_ da unidade e das dependências

   - definir retornos e exceções
   - definir expectativas

2. executar objeto do teste com suas entradas

3. asserções
   - comparar saída obtida com a esperada
   - verificar as expectativas das dependências

---

## Exemplos de código

1. Exemplo de teste usando classe Stub
   - `test_lista_cpfs_inadimplentes_stub()`

2. Exemplo de teste usando classe Fake
   - `test_lista_cpfs_inadimplentes_fake()`

3. Exemplo de teste usando Mock
   - `test_lista_cpfs_inadimplentes_mock()`

```
Executar testes básicos python:
# source ~/.virtualenvs/venv/bin/activate
# python run_unit_tests.py
```

---

Atenção para não testar o _stub/fake/mock_ ao invés da unidade.

```python
def test_list_cpfs_inadimplentes():
    # setup
    debito_repo = Mock()
    debito_repo.lista_debitos_por_cpfs.return_value = [
        {'id': 1, 'cpf': '15150373044', 'pago': False,  'data': date(2022, 1, 1)}
    ]

    # execução
    mock_return = debito_repo.lista_debitos_por_cpfs(['15150373044', '21426399090'])

    # expectativas e asserções
    assert mock_return == [
        {'id': 1, 'cpf': '15150373044', 'pago': False,  'data': date(2022, 1, 1)}
    ]
```

---

# E o não-determinismo?

Algumas fontes de não-determinismo:

- base de dados, serviços externos ou estado global/variáveis de classe/_static_
- `Date.now()` e `datetime.date.today()`
- `Math.random()` e `random.random()`
- concorrência e paralelismo

---

## Como tratar o não-determinismo?

Quando for uma dependência implícita:
- transformar em dependência explícita
- criar abstrações e _factories_ que possam ser substituídas por classes _mocks_ ou _fakes_
- usar recursos dos _frameworks_, _eg:_
  - python `@freeze_time`
  - js `jest.setSystemTime`

<br>

Quando se tratar de concorrência/paralelismo:
- :cry:

---

# E os requisitos não-funcionais?

Desempenho, tempo de resposta, quantidade de conexões, _etc_?

Não são avaliados por testes unitários, mas podem ser avaliados por [testes de sistema](https://www.toolsqa.com/software-testing/istqb/system-testing/) ou [testes de integração](https://www.toolsqa.com/software-testing/integration-testing/).

---

# Quanto mais testes melhor!!!

### :fire: _Hot take_ :fire:

Opa, não é bem assim!
A quantidade de entradas possíveis de um sistema é grande demais (praticamente ilimitada).
Testes demais vão ter um alto custo de manutenção.
Portanto temos que escolher quais testes fazer.

Vamos dar preferência a "testes bons".

---

## O que faz um teste "bom"?

<br>

Testes bons são aqueles com maior probabilidade de revelar algum defeito.
Vários testes que testam a mesma coisa tem pouco valor.

---

## Como saber se o teste é bom?

Tendo critérios de escolha, por exemplo:

- Critérios funcionais (_aka [black-box](https://en.wikipedia.org/wiki/Black-box_testing)_): derivados da funcionalidade
- Critérios estruturais (_aka [white-box](https://en.wikipedia.org/wiki/White-box_testing)_): derivados da estrutura do código

<br>

Bons testes variam:

- cenários
- tipos de erros
- fluxos de execução

---

### Critérios Funcionais

Os testes são criados cobrindo as funcionalidades do sistema: especificação, requisitos funcionais, _user stories_, _use cases_, regras de negócio...
<br>

Algumas [técnicas de critérios funcionais](https://en.wikipedia.org/wiki/Black-box_testing#Test_design_techniques) ajudam na escolha:

- partições em classe de equilalência (_ie_ separar a entrada em categorias)
- análise de valor limite
- tabelas de decisão
- máquina de estados
- erros comuns (_string_ vazia, _undefined_, _None_, data inválida, valores fora da faixa...)

```
executar testes básicos typescript
# npm test
```

---

### Critérios Estruturais

Critérios estruturias medem % de cobertura do código (_white-box_).

- todas as funções/métodos
- todas as linhas
- todos os fluxos de controle (_branches_)
- ...

Ajudam a descobrir testes interessantes que não estão sendo feitos.

```
1 - grafos dos exemplos: app.dot e cpf.dot
2 - observar HTML de cobertura dos testes triviais (py e ts)
3 - descomentar o critério '--cov-branch' do run_unit_tests.py
```

---

## Antes & depois
![height:320px](img/antes-depois.jpg)

:eyes: Observar o incremento da cobertura nos arquivos HTML.
```
- grafo exemplo: app-simples.dot
- descomentar testes criados usando critérios estruturais em py e ts
python: branch 1F e 2F
typescript: branch 1T
```
---

## Qual é a cobertura ideal?

---

![bg](img/cobertura-ideal.webp)
![](#000)

### A cobertura ideal:

### TL;DR 80%

---

## :clown_face: :clown_face: :clown_face:

<br>

Não tem fórmula mágica :worried:
Vale o bom senso e XP

<br>

Referência: https://testing.googleblog.com/2010/07/code-coverage-goal-80-and-no-less.html

---

## OK, mas conseguimos cobertura de 100%! pronto?

:grimacing:

<br>

Mesmo com 100% de cobertura\* ainda podemos melhorar usando critérios funcionais complementares.

### \* em qualquer critério

<style scoped>
h3 {
  font-size: 18px;
}
</style>

---

## Lá e de volta outra vez

- exemplo final python

- exemplo final typescript

---

![bg](img/thats_all_folks.webp)
