# Notificador

O Notificador é uma aplicação FastAPI que serve como uma demonstração de um sistema de notificações. Essa aplicação é capaz de enviar notificações tanto por e-mail quanto por webhook (integrações com ferramentas como Mattermost e Slack). Além disso, o projeto ilustra o uso do RabbitMQ com a biblioteca aio-pika e também do MongoDB.

## Como Usar

### Clonando o Repositório

Clone o repositório para a sua máquina local:

```shell
git clone https://github.com/seu-usuario/notificador.git
cd notificador
```

### Configuração do Ambiente

Certifique-se de que você possui o Docker e o Docker Compose instalados. 

Crie um arquivo `.env` no diretório raiz do projeto. Você pode copiar o arquivo `.env.sample` disponível e editá-lo conforme necessário.

Se você planeja utilizar o serviço de envio de e-mail, configure uma conta no SendGrid e forneça as seguintes variáveis de ambiente no arquivo `.env`:

```env
SENDGRID_API_KEY=SuaChaveAPI
SMTP_REMETENTE=seu-email@example.com
```

### Executando o Projeto

No terminal, execute o seguinte comando para construir e iniciar os contêineres Docker:

```shell
docker-compose up -d --build
```

Uma vez que a aplicação esteja em execução, a documentação Swagger dos endpoints estará automaticamente disponível em `http://localhost:8080/docs`. Você pode usar essa documentação para testar os endpoints.

## Endpoints

A aplicação oferece os seguintes endpoints:

### 1. Cadastro de Notificações

- Método: POST
- URL: `http://localhost:8080/notificacoes`
- Payload: JSON com os seguintes atributos:
  - `type`: Tipo de notificação, atualmente suporta os valores "email" e "webhook".
  - `email`: E-mail que deve receber a notificação (obrigatório se o `type` for "email").
  - `webhook`: URL do webhook para notificar (obrigatório se o `type` for "webhook").
  - `titulo`: O título da notificação.
  - `mensagem`: A mensagem que será notificada.

### 2. Listagem de Notificações

- Método: GET
- URL: `http://localhost:8080/notificacoes`
- Resposta: Retorna o ID da notificação, o título e o status. O status pode ser "PENDENTE", "ENVIADA" ou "FALHA_AO_ENVIAR".

## Funcionamento Interno

Quando o endpoint de cadastro de notificações é chamado, a aplicação salva os detalhes da notificação no MongoDB com o status "PENDENTE". Além disso, ela publica uma mensagem na fila "disparo_notificacao" do RabbitMQ utilizando a biblioteca aio-pika e, em seguida, retorna uma resposta.

A própria aplicação consome a fila "disparo_notificacao", onde um consumidor assíncrono lida com o envio real da mensagem, seja por webhook ou por e-mail. Após o envio da notificação, o consumidor atualiza o status no MongoDB, marcando-o como "ENVIADA" em caso de sucesso ou "FALHA_AO_ENVIAR" em caso de erro. Tudo isso é feito de forma assíncrona com a ajuda da biblioteca asyncio.
