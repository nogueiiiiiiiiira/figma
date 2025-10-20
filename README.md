# READE (nao pronto, aguardandos ats)

# MINI MUNDO:
Atualmente, o controle de presença do Hospital Cajuru é realizado com assinatura em folha de papel, o que gesta problemas como perda de registros, dificuldade de cálculo de horas e falta de um histórico organizado e dinâmico e moderno. O projeto tem como objetivo criar um sistema de controle de ponto digital legal. Esse terminal permite ao voluntário registrar sua chegada e saída de forma rápida e confiável, armazenando os dados para acesso e gestão para alguém autorizado cuidar.

# REQUISITOS FUNCIONAIS:
- O sistema deve oferecer duas formas de identificação no terminal: leitura de cartão RFID e digitação de um código numérico (ID ou CPF) via teclado matricial.
- O sistema deve registrar cada batida de ponto, armazenando a data, a hora, o tipo (entrada ou saída) e a identificação do voluntário/funcionário.
- O sistema web deve permitir o cadastro, consulta, edição e exclusão de voluntários (CRUD)
- O sistema web deve permitir o cadastro, consulta, edição e exclusão de usuários (CRUD).
- O sistema deve enviar os registros de ponto do terminal para o banco de dados em tempo real.

# REQUISITOS NÃO FUNCIONAIS:
- A interface web deve ser intuitiva e de fácil utilização.

# ARQUITETURA DO SISTEMA (BANCO DE DADOS):
Serão utilizadas três tabelas principais:
- VOLUNTARIOS: armazena id_voluntario (chave primária), nome, cpf, telefone, data_cadastro, etc.
- REGISTROS_PONTO: armazena id_registro (chave primária), data_hora, tipo (entrada/saída) e id_voluntario (chave estrangeira para VOLUNTARIOS), etc.
- USUARIOS: armazena id_usuario (chave primária), senha (criptografada), etc.

OBS: Considerando outras tabelas para deixar tudo bonitinho.

# IDEIA DO SISTEMA EMBARCADO:
O terminal físico será construído com uma placa ESP32. A identificação do voluntário pode ocorrer de duas maneiras:
1.  Através da aproximação de um cartão RFID ao leitor.
2.  Através da digitação de um código numérico (ID ou CPF) em um teclado matricial 4x4.
Um display LCD fornece feedback ao usuário, exibindo mensagens de confirmação.
A ESP32, programada em MicroPython, processa a identificação e publica imediatamente uma mensagem contendo o ID do voluntário e o tipo de registro em um tópico MQTT.

IDEIA DA INTERFACE WEB:
A interface web será um painel administrativo com acesso restrito por login e senha. Mas também terá uma parte onde qualquer um pode registrar manualmente o ponto batido, desde que o ID/CPF seja encontrado no sistema.
A integração com o terminal físico (ESP32) ocorre através do protocolo MQTT. O servidor web recebe as mensagens de ponto publicadas pela ESP32 e guarda elas no banco de dados.
