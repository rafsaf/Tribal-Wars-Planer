# Guia de Planos de Ruína

Neste guia, você aprenderá a planejar ações de destruição, especificamente voltadas para as fases posteriores do mundo. Nota: Este guia pressupõe conhecimento completo de [Primeiros Passos com o Planejador](./../first_steps/index.md)! Também é recomendado ler primeiro os dois guias curtos anteriores nesta seção, ou seja, [Como Inserir e Salvar Metas de Ação](./two_regions_of_the_tribe.md) e [As Duas Regiões da Tribo, ou seja, O que é a Frente e a Retaguarda](./two_regions_of_the_tribe.md).

!!! hint

    Sempre comece a planejar qualquer ação nesta página contando todas as tropas e dividindo-as em tropas da Frente e da Retaguarda, de acordo com a natureza do plano específico. Para isso, use a aba 1. Unidades Disponíveis, e os resultados são apresentados em uma tabela abaixo das metas.

A ação será totalmente criada no campo **Unidades de Cerco**, ao lado das Metas. As configurações na aba {==6. Unidades de Cerco==} são muito simples, onde determinamos principalmente a ordem dos edifícios a serem destruídos e o número máximo de catapultas nos ataques de destruição (o mínimo é 50).

Exemplo de Metas de Destruição e Resultados da Tabela, com 3 unidades de ataque e \*50 unidades de cerco:

![alt text](image-24.png){ width="600" }

Exemplo de Configurações de Ação de Destruição, visando 3 edifícios visíveis nesta ordem:

![alt text](image-25.png){ width="600" }

(Nota: 50 unidades de cerco não significam necessariamente que este número exato será planejado!)

Você pode estimar o número de unidades de cerco disponíveis usando a aba {==1. Unidades Disponíveis==} e matemática simples. Após cada atualização, você pode encontrar o número total de catapultas prontas para o planejamento na tabela em **Número de Todas as Catapultas Disponíveis**. Você só precisa decidir para quantas metas elas serão suficientes.

Exemplo de uma mini-ação planejada, com vários números de catapultas de 200 a 50:

![alt text](image-26.png){ width="600" }

## Seleção Ótima de Catapultas para Destruição

Vejamos como o Planejador se comporta para um MÁXIMO de 200 catapultas. Se houver aldeias com essa quantidade, elas serão priorizadas (acima de 100 catapultas) e, quando se esgotarem, o restante será preenchido com quantidades menores—150, 100, 75, 50. Além disso, quando, por exemplo, restarem 10 níveis de um edifício após vários ataques, o Planejador atribuirá o último ataque com 50 catapultas em vez de uma quantidade maior (mesmo que disponível) para economizar catapultas.

## Unidades de Ataque Antes das Unidades de Cerco

Quanto às unidades de ataque, cujo número pode ser especificado para entrar antes dos ataques de destruição, seu papel é limitado ao de unidades de ataque padrão. Elas não fazem parte do algoritmo que lhes atribui um número específico de catapultas e um edifício a ser destruído—embora, teoricamente, a mesma aldeia possa enviar tanto unidades de ataque antes do cerco quanto unidades de cerco nos ataques planejados. Estes são processos separados e, na versão atual, não é possível que as unidades de ataque "ajam" como uma das unidades de cerco.

## Ordem de Destruição de Edifícios

Nas configurações {==6. Destruição==}, podemos alterar a ordem dos edifícios a serem destruídos. É importante lembrar que os edifícios não incluídos nesta lista serão ignorados, e o algoritmo para em dois casos—ou não há mais catapultas para planejar ou todos os edifícios listados já foram destruídos. Isso significa que, mesmo que decidamos escrever `000|000:0:1000`, 1000 unidades de cerco provavelmente não serão planejadas—uma vez que os edifícios listados sejam destruídos, o Planejador passa para os próximos passos (por exemplo, a próxima meta, etc.).

## Vejo 10.000 Catapultas Disponíveis. Quantas Metas São?

A resposta é: depende. Principalmente da ordem de construção escolhida. Vamos supor que apenas um edifício seja escolhido, **[ Ferraria ]**. Neste caso, 200-250 catapultas (por exemplo, 200 e 50 ou 100, 100, ou 50, 50, 50, 50, etc.) são suficientes para destruir uma aldeia, então você pode planejar 40-50 metas. Se dois edifícios forem escolhidos, **[ Ferraria, Fazenda ]**, você precisará de 200-250 catapultas para a Ferraria e 500-700 catapultas para a Fazenda (por exemplo, 14x 50, ou 5x 100, 4x 150, 3x 200 catapultas ou muitas outras combinações), o que significa 700-950 catapultas por aldeia, ou 10-14 metas. Abaixo está uma tabela simples para edifícios de 30 níveis (como Fazendas, Armazéns, todos os edifícios eco) e edifícios de 20 níveis (Quartel General, Ferraria) para ajudar a calcular quantas metas são possíveis.

|                        | Número de Catapultas Necessárias para a Destruição Completa do Edifício |
| ---------------------- | ----------------------------------------------------------------------- |
| Edifícios de 20 níveis | 200-250                                                                 |
| Edifícios de 30 níveis | 500-700                                                                 |

## Resumo

Lembre-se que, em sua essência, o planejamento é baseado em um algoritmo guloso simples, e assim o Planejador **SEMPRE** atribui unidades de cerco, fakes ou unidades de ataque **ALEATORIAMENTE** de uma maneira muito semelhante. Se você quer que unidades de ataque ou de cerco sejam indistinguíveis de fakes, você precisa planejar muitos fakes. Ao planejar a destruição, vale a pena habilitar a opção **Fakes de Todas as Aldeias** na {==Aba 3. Configurações Padrão da Ação==}, que, ao contrário da configuração padrão, atribui fakes de todas as aldeias da retaguarda.

Em conclusão, considere o número de catapultas (e quantos edifícios vale a pena destruir; talvez apenas a Fazenda + prefeitura + Ferraria?) e planeje muitos fakes. Aproveite a demolição!

---

Me avise se precisar de outros detalhes ou alterações!
