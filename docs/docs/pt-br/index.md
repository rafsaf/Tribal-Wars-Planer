# Documentação do Planejador de Guerras Tribais

## Introdução

Esta é a documentação para o site [plemiona-planer.pl](https://plemiona-planer.pl) – um projeto ambicioso para o [plemiona.pl](https://plemiona.pl), que começou em janeiro de 2020 após a atualização do jogo para a versão 8.192 em novembro de 2019. A atualização introduziu a capacidade para os administradores da tribo coletarem dados sobre os jogadores e suas unidades.

- [1. Mundo de Teste](./first_steps/index.md) - uma seção dedicada a explorar o site sem a necessidade de instalar nada ou mesmo ter uma conta de jogo ativa. Permite o planejamento de ações em um Mundo de Teste especialmente preparado.
- [2. Instalação dos scripts necessários](./scripts/army_and_defence_collection.md) - para uso no mundo real e planejamento de ações para uma tribo real, é necessário um script para coletar dados da tribo (opcionalmente, um segundo script ajuda a enviar mensagens aos jogadores).
- [3. Guias](./primary/write_outline_targets.md) - 6 artigos extensos sobre tópicos específicos relacionados ao planejamento de ações.
- [4. Avançado](./primary/write_outline_targets.md) - uma descrição de todas as abas e opções na aba principal "Planejador".

## Perguntas e Respostas

### Sobre o Site

> O que é este site e para quem ele é e não é?

Este site é para **administradores de tribos** e seus coordenadores de ataque que têm acesso aos dados dos jogadores. Usando os dados da tribo e inserindo os alvos da ação e ajustando as configurações, um coordenador pode gerar um plano de ataque e enviar os alvos aos jogadores (através de um link para o site ou diretamente em uma mensagem do jogo). A matemática usada no site e as muitas opções permitem planejar praticamente qualquer ação em qualquer estágio do jogo, economizando o tempo do planejador.

> O que o plemiona-planer NÃO é?

NÃO é uma ferramenta ilegal, um bot de jogo ou qualquer script que automatize ações no jogo. O site NÃO se conecta ao jogo para nenhum outro propósito além de buscar dados mundiais publicamente disponíveis. Você NUNCA será solicitado a fornecer sua senha do jogo!

### Pagamentos

> O plemiona-planer é pago?

O site é gratuito. No entanto, você pode adquirir uma assinatura de conta premium, que permite planejar mais de 40 alvos em um único plano de ataque e concede acesso a dados não utilizados de ações planejadas anteriormente (para uso em ações futuras). Não há diferenças na funcionalidade, qualidade do algoritmo ou velocidade. Este modelo ajuda a manter o serviço, e a taxa pode ser dividida entre os membros da tribo. Não há necessidade de mais de uma conta por tribo, exceto em casos de problemas **óbvios!** com o compartilhamento de contas. O site não se responsabiliza por perdas devido a acesso não autorizado, roubo de conta ou compartilhamento de senhas com oponentes. O proprietário da conta deve pesar os prós e os contras antes de fornecer sua senha a terceiros.

> Como é possível que o código do aplicativo seja aberto e esteja disponível no GitHub?
>
> Por que pagar por uma assinatura se você pode usar o código gratuitamente?

Eu sou um defensor do [software de código aberto](https://opensource.com/resources/what-open-source)! É verdade, você pode optar por não pagar e usar o código do site e o resultado de anos de trabalho de muitos usuários dedicados. De graça, e assim permanecerá :) Isso também reflete minha confiança na segurança e na matemática usada no planejamento – não há nada a esconder. No entanto, a conveniência de planejar de qualquer local e o acesso online aos resultados do planejamento para os membros da tribo são inestimáveis. Configurar seus próprios servidores requer conhecimento especializado, custos consideráveis e manutenção contínua, atualizações, etc. A taxa de assinatura também cobre o tempo necessário para corrigir bugs, ajudar os usuários com problemas ou desenvolver novos recursos. Tudo isso não seria possível sem o apoio dos usuários. Obrigado a todos que apoiam este projeto.

### Dados

> Meus dados estão seguros?

O site está online desde meados de 2020. Durante este tempo, não houve nenhum incidente de segurança. O modelo de negócios atual sustenta os servidores. Os dados enviados pelos usuários são de sua responsabilidade e nunca serão vendidos ou compartilhados com terceiros.

> Posso criar planos de ataque no seu Planejador sem ter acesso aos dados da tribo?

Não, o fornecimento de dados é obrigatório. Você deve estar na administração da tribo, e seus membros precisam habilitar as configurações apropriadas para compartilhar dados. Existe um mundo de teste onde você pode experimentar o site sem acesso aos dados da tribo.

### Plano de Ataque

> Olá, por que o Planejador não está delineando todas as minhas unidades ofensivas? Acho que já mudei tudo nas configurações, mas ele continua deixando 2.7k de tropas ofensivas sem uso…

Pode haver muitas razões, principalmente as configurações da ação na aba [1. Tropas Disponíveis e descrição da tabela](./advanced/1_available_troops_and_table.md), como pular algumas aldeias da linha de frente ou distantes perto da borda. Menos frequentemente, é devido aos [3. Parâmetros do Plano de Ataque](./advanced/3_outline_parameters.md). O Planejador não verifica completamente os parâmetros impensados e **permite erros**. Por exemplo, se as configurações da linha de frente indicarem que toda a tribo está na frente, mas o usuário definir unidades ofensivas apenas da linha de trás, o aplicativo delineará tal ação, mesmo que nenhuma unidade ofensiva seja incluída.

### Bônus Noturno

> Como o algoritmo funciona para evitar ataques noturnos o máximo possível?

O intervalo de números naturais de 0 a 23, com 0-7 tendo a pior pontuação = 1, as bordas do intervalo pontuação = 2 e as horas completamente "seguras" pontuação = 3, tudo envolvido em módulo 24. [Código aqui](https://github.com/rafsaf/Tribal-Wars-Planer/blob/708b2677a3ee64d2fb8fc50eb8d7601811260dff/utils/write_ram_target.py#L297).

Isso deve ser feito para cada alvo individualmente através de todas as aldeias aliadas, primeiro calculando a distância em campos.

### Scripts

> Olá, não entendi muito bem como funciona o script de envio de alvos. Depois de instalá-lo na barra de ferramentas, nada acontece na interface das tribos.

Veja [Script para envio de mensagens](./scripts/sending_messages.md). É um **script de navegador**, não para a barra de ferramentas do jogo. É usado na nova visualização de mensagem se houver parâmetros especialmente adicionados na URL. [Verifique o ponto 11 na aba de resultados](./first_steps/step_7_results_tab.md).

### Legal e Licença

> Posso usar o código do plemiona-planer do GitHub?

Sim! Você pode fazer qualquer coisa dentro da **Licença Apache 2.0** – configurar o Planejador localmente, usar forks e implantá-los você mesmo. Você pode usar o código copiado do repositório do GitHub para suas ferramentas (sob a Licença Apache 2.0, o que significa SEM remover o cabeçalho da licença). Eu NÃO concordo com a falsificação da marca plemiona-planer.pl, o uso do logotipo rafsaf.pl ou meu nome na política de privacidade em produtos ou projetos baseados no plemiona-planer.pl.
