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

Durante a implementação das funcionalidades, a RFC do protocolo IRC(https://datatracker.ietf.org/doc/html/rfc1459) foi utilizada como base para esclarecimentos. A linguagem Python foi utilizada para a implementação, valendo apenas do módulo “sockets” e “threading” como base. O projeto foi desenvolvido em um ambiente da família “unix-like”, portanto, para evitar possíveis inconsistências, execute o projeto em um ambiente linux, utilizando o terminal de sua preferência.

As senhas são armazenadas de forma encriptada em uma lista, através da criptografia SHA-256, aumentando a segurança. Ao conectar-se ao servidor, o usuário é automaticamente adicionado à sala “Lobby”, a sala principal do servidor.

Importante: Para executar os comandos /ban, /unban e /kick uma senha de administrador é requerida, a senha é exibida apenas ao operador do servidor. Para facilitar a usabilidade, a senha padrão foi definida como: “adminpassword”. Além disso, para cada comando executado no servidor uma mensagem é exibida no terminal do operador do servidor.

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

  Este comando tem a função de criar uma nova sala de chat no servidor. Por padrão, é perguntado ao usuário qual o nome da sala que será criada e por fim, em que sala o usuário deseja entrar.

- [x] /JOIN

  O comando /join têm por função principal inserir o usuário em uma sala. Se o comando for executado com o usuário estando em outra sala, este é retirado da lista da sala original e adicionado na sala em que deseja entrar.

- [x] /DELETE

  Este comando tem por função deletar alguma sala de chat criada no servidor. Se houver usuários na sala, eles serão movidos para a sala “Lobby” e a sala será excluída.

- [x] /LIST

  Este comando tem por função principal listar as salas de chat disponíveis no servidor e a quantidade de usuários em cada uma.

- [x] /LISTUSERS

  Através deste comando é possível visualizar quais usuários estão conectados ao servidor através dos nicknames.

- [x] /LISTBANNED

  Através deste comando é possível visualizar todos os usuários que foram banidos do servidor. Todos os nomes exibidos estão presentes no arquivo “bans.txt”.

- [x] /BAN

  Este comando tem a função de banir permanentemente um usuário de conectar-se ao servidor. Para utilizá-lo é necessário informar a senha “adminpassword”, por tratar-se de uma ação de usuário administrador. O usuário banido é então adicionado ao arquivo “bans.txt” e não consegue conectar-se ao servidor enquanto seu nickname estiver na lista de banimento.

- [x] /UNBAN

  O comando /unban tem por finalidade desbanir um usuário do servidor, fazendo com que o nickname seja retirado da lista de banimento e o usuário consiga conectar-se novamente ao servidor. Assim como no comando para realizar o banimento, a senha de administrador é requerida para executar o comando.

- [x] /LEAVE

  O comando /leave tem por função fazer com que o usuário que o inseriu saia da sala em que está no momento e seja automaticamente adicionado à sala “Lobby”, a sala principal.

- [x] /EXIT

   Este comando tem a função de encerrar a conexão do usuário com o servidor. Para executá-lo, uma confirmação é solicitada(sim/nao) e a senha do usuário é necessária para confirmar a ação. Após a conexão ser encerrada, as informações do usuário são excluídas do servidor.

- [x] /KICK

  Este comando tem por função principal “kickar” um usuário da sala em que ele está. Para sua execução, a senha de administrador é necessária.

- [x] /TIME

  Este comando tem por função principal exibir o horário no momento em que é executado.

- [X] /HELP

  Através deste comando o menu com todos é exibido na tela do usuário.

***

## 4. Autores 🤖

| <img src="https://avatars.githubusercontent.com/u/62662399?v=4" alt="Murilo" width="150"/> | <img src="https://avatars.githubusercontent.com/u/69048604?v=4" alt="Joao" width="150"/> | <img src="https://avatars.githubusercontent.com/u/65295232?v=4" alt="Vitor" width="150"/> | <img src="https://avatars.githubusercontent.com/u/4358822?v=4" alt="Guilherme" width="150"/> |
|:-------------------------------------------------------------------------------------------:|:-------------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|
| [Murilo Gomes Munhoz](https://github.com/MuriloGomesMunhoz)                                 | [João Pedro Rosa Cezarino](https://github.com/akajhon)                                      | [Vitor Martins Oliveira](https://github.com/vihmar)                                         | [Guilherme Brigagão Cabelo](https://github.com/rmgg)                                       |
| R.A: 22.120.035-5                                                                           | R.A: 22.120.021-5                                                                           | R.A: 22.120.067-8                                                                           | R.A: 22.120.071-0                                                                          |
