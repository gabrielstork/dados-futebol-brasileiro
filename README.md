# dados-futebol-brasileiro

Colete dados do site oficial da CBF (Confederação Brasileira de Futebol).

[robots.txt](https://www.cbf.com.br/robots.txt)

![Exemplo](https://github.com/gabrielstork/dados-futebol-brasileiro/blob/main/images/xlsx_file_example.PNG)

## Como utilizar?

Antes de tudo, você deve clonar esse repositório para a sua máquina local, uma das maneiras é copiando e colando em seu terminal:

```sh
git clone https://github.com/gabrielstork/dados-futebol-brasileiro.git
```

Após clonar o repositório, caso você não tenha as bibliotecas necessárias (listadas no arquivo `requirements.txt`), digite em seu terminal:

```sh
cd dados-futebol-brasileiro
pip install -r requirements.txt
```

Pronto! Agora você já pode utilizar o código!

Existem duas maneiras para isso:

* Movendo o arquivo `brazilian_soccer.py` para o seu diretório de trabalho e importando o necessário para o seu código.
* Modificando o próprio arquivo `brazilian_soccer.py`.

### Exemplo

Instanciando a classe.

```python
brasileirao_2018 = Brasileiro(2018, 'A')
```

Obtendo os dados.

```python
brasileirao_2018.get_data()
```

Salvando os dados.

```python
brasileirao_2018.save_data('brasileirao_2018.csv')
```
