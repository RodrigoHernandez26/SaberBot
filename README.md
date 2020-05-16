# SaberBot
SaberBot é um bot brasileiro de moderação para o Discord!

## Como adicionar ao seu servidor:
Você pode adicionar o SaberBot ao seu server clicando [aqui](https://discordapp.com/oauth2/authorize?client_id=705878925363904543&scope=bot&permissions=8).

## Pré-requisitos:
Utilizamos o Windows 10, talvez não funcione em outros OS.
```
* Python 3.6.9 ou superior.
* Pip 9.0.1 ou superior.
* Node.js 12.16.2 ou superior.
* Npm 6.14.4 ou superior.
* MongoDB
* MySQL
```
Todos os pacotes do pip estão em `./requirements.txt` e os pacotes do npm estão em `./api/package.json`.

## Instalação
1. [Python](https://www.python.org/downloads/)
2. [Pip](https://pip.pypa.io/en/stable/installing/)
3. [Node.js e Npm](https://nodejs.org)
4. Para instalar as dependencias do Bot:
    ```
    pip install -r requirements.txt
    ```
5. Para instalar as dependencias da API:
    ```
    npm install
    ```
6. [MongoDB](https://www.mongodb.com)
7. [MySQL](https://www.mysql.com/downloads/)

## Criação de arquivos
Antes de iniciar a hospedagem, você precisa criar 3 arquivos `settings` em `./bot/settings`, `./api`, `./web/settings`. Em cada uma dessas pastas, tem um `.example` que você deve usar como guia.

A query de criação do MySQL está em `./bot/settings/bot.sql`.

## Autor
* [Lucas Módolo](https://github.com/LucasModolo22)
* [Rodrigo Hernandez](https://github.com/RodrigoHernandez26)

## Licença
Esse projeto está licenciado sob a [MIT License](https://github.com/RodrigoHernandez26/Saber-Bot/blob/master/LICENSE).