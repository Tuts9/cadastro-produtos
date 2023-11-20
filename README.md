# Sistema de cadastro de produtos em Banco de Dados com Interface Gráfica em Python

Este é um script que implementa um sistema que adiciona produtos a um banco de dados local, o sistema permite o usuário inserir todas as informações necessárias e cadastrar o produto

## Pré-requisitos

-Python 3.x

-Biblioteca `Customtkinter` (é necessário instalá-la)

-Biblioteca Tkinter (normalmente incluída na instalação padrão do Python)

-Biblioteca Sqlite3 (normalamente incluída na instalação padrão do Python)

-Biblioteca `FPDF` (é necessário instalá-la)

-Biblioteca `Pandas` (é necessário instalá-la)

-Biblioteca `Unicodedata` (é necessário instalá-la)

## Como usar

1. Certifique-se de que os pré-requisitos estejam instalados.

2. Clone o repositório ou copie o código em um arquivo Python (.py).

3. Execute o arquivo Python.

4. O sistema será executado em uma janela gráfica.

5. Digite todas as informações necessárias sobre o produto que deseja adicionar.

6. Clique em cadastrar e o sistema irá criar um banco de dados no mesmo diretório que o seu arquivo Python estiver.

7. Automaticamente o sistema irá listar o produto que acabou de ser cadastrado no espaço em branco logo a baixo dos campos de entrada.

8. Você poderá adicionar quantos produtos quiser e sempre que clicar para cadastrar o sistema irá verificar se já existe o arquivo de banco de dados (.db), se já existir ele apenas adicionará juntos aos outros já incluídos.

9. Também foi adicionada uma função de pesquisa para que ajude o usuário a não precisar ficar rolando a lista completa.

10. Ao clicar no botão de pesquisa o sistema irá esconder os campos de entrada para cadastro e mostrará apenas um campo para você digitar o nome do produto que deseja procurar.

11. Para o uso dos dados inseridos no programa foi adicionado duas funcionalidades, uma para criar um arquivo (PDF) e outra para criar um arquivo (Excel) que ficarão no mesmo diretório que o arquivo Python estiver sendo executado.

## Estrutura do código

- O códogo é estruturado em classes e métodos para melhor compreensão, manutenção e alteração.

- A classe `Produtos` é a principal e contém toda a lógica do sistema e a interface gráfica.

- O sistema usa a Biblioteca `Unicodedata` para remover eventuais acentos que possam atrapalhar ao salvar os produtos no banco de dados, e através de uma função que é usada apenas para remover os acentos contidos no texto apresentado a ela.

- A interface gráfica é criada usando a biblioteca `Customtkinter` contendo `frames` para organização dos elementos.

## Licença

Este código é disponibilizado sob a licença [MIT](https://opensource.org/licenses/MIT), o que significa que você é livre para usá-lo, modificá-lo e distribuí-lo da maneira que desejar, desde que mantenha o aviso de direitos autorais original e não responsabilize os autores por qualquer dano ou perda relacionada ao uso deste código.
