### CE5320 - TÓPICOS AVANÇADOS DE REDES DE COMPUTADORES - CENTRO UNIVERSITÁRIO FEI
```bash
 _____  _____ ______   _____  _____  _____  _   __ _____  _____   _____  _   _   ___  _____ 
|_   _|/  __ \| ___ \ /  ___||  _  |/  __ \| | / /|  ___||_   _| /  __ \| | | | / _ \|_   _|
  | |  | /  \/| |_/ / \ `--. | | | || /  \/| |/ / | |__    | |   | /  \/| |_| |/ /_\ \ | |  
  | |  | |    |  __/   `--. \| | | || |    |    \ |  __|   | |   | |    |  _  ||  _  | | |  
  | |  | \__/\| |     /\__/ /\ \_/ /| \__/\| |\  \| |___   | |   | \__/\| | | || | | | | |  
  \_/   \____/\_|     \____/  \___/  \____/\_| \_/\____/   \_/    \____/\_| |_/\_| |_/ \_/                      
```
<p align="center">
  <img alt="Python" src= "https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img alt="Sockets" src= "https://img.shields.io/badge/-SOCKETS-blue"/>
  <img alt="Sucess" src= "https://img.shields.io/badge/-SUCCESS-green"/>
</p>

***

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="https://github.com/akajhon/HTTP_Sockets_Server/edit/main/README.md#1-introdu%C3%A7%C3%A3o-">Introdução</a>
    </li>
    <li>
      <a href="https://github.com/akajhon/HTTP_Sockets_Server/edit/main/README.md#2-rodando-localmente-">Rodando Localmente</a>
    </li>
    <li>
      <a href="https://github.com/akajhon/HTTP_Sockets_Server/edit/main/README.md#2-requisi%C3%A7%C3%A3o-via-linha-de-comando-">Requisição via TELNET</a>
    </li>
    <li>
      <a href="https://github.com/akajhon/HTTP_Sockets_Server/edit/main/README.md#6-autores-">Autores</a>
    </li>
  </ol>
</details>

***

## 1. Introdução 📘

O projeto tem por objetivo a implementação de um servidor de chat baseado no protocolo TCP e imitando o protocolo IRC (Internet Relay Chat). O servidor deve ser  capaz de interpretar alguns comandos recebidos através de solicitações via linha de comando(telnet), ter suporte á conexão de múltiplos usuários, diversas salas de bate-papo, autenticação, entre outras funções . O servidor deve ser capaz de responder a essas solicitações corretamente.

Durante a implementação das funcionalidades, a RFC do protocolo IRC(https://datatracker.ietf.org/doc/html/rfc1459) foi utilizada como base para esclarecimentos. A linguagem Python foi utilizada para a implementação, valendo apenas do módulo “sockets” e “threading” como base.

***

## 2. Rodando localmente 🏠

Clone o projeto

```bash
  git clone https://github.com/akajhon/TCP_MultiChat_Server
```

Entre no diretório do projeto

```bash
   cd TCP_Multichat_Server
```
Instale as dependências do projeto

```bash
   pip install requirements.txt
```

Inicie o servidor

```bash
  phyton3 Multichat_server.py
```

Para entrar no servidor digite: 

```bash
  telnet localhost 8000
```

***

## 3. Requisição via TELNET 👨‍💻

Após a conexão via telnet ser realizada, a tela inicial do servidor é exibida solicitando nome, nickname e senha. 

<p align="center">
  <img src="https://github.com/akajhon/TCP_MultiChat_Server/blob/main/images/img01.png" alt="Telnet" width="450" height="450"/>
</p>

Os comandos implementados foram: 
- [x] /CREATE
- [x] /LOGIN
- [x] /DELETE
- [x] /LIST
- [x] /LISTUSERS
- [x] /LISTBANNED
- [x] /BAN
- [x] /UNBAN
- [x] /QUIT
- [x] /EXIT
- [x] /KICK
- [x] /TIME

## 4. Autores 🤖

| <img src="https://avatars.githubusercontent.com/u/62662399?v=4" alt="Murilo" width="150"/> | <img src="https://avatars.githubusercontent.com/u/69048604?v=4" alt="Joao" width="150"/> | <img src="https://avatars.githubusercontent.com/u/65295232?v=4" alt="Vitor" width="150"/> | <img src="https://avatars.githubusercontent.com/u/4358822?v=4" alt="Guilherme" width="150"/> |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [Murilo Gomes Munhoz](https://github.com/MuriloGomesMunhoz)                                 | [João Pedro Rosa Cezarino](https://github.com/akajhon)                                      | [Vitor Martins Oliveira](https://github.com/vihmar)                                         | [Guilherme Brigagão Cabelo](https://github.com/rmgg)                                       |
| R.A: 22.120.035-5                                                                           | R.A: 22.120.021-5                                                                           | R.A: 22.120.067-8                                                                           | R.A: 22.120.071-0                                                                          |
