# Roteiro de Coleta de Exército e Defesa

| Servidor          | Fórum do Tribal Wars                                                                                                                                                 | Permitido | Código                                                                                                                 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------- |
| tribalwars.net    | [https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/](https://forum.tribalwars.net/index.php?threads/collect-troops-script.292893/)         | SIM       | [Código no GitHub (v2.1)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-09-2/src/collect_troops_v2.1.ts)  |
| plemiona.pl       | [https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/](https://forum.plemiona.pl/index.php?threads/zbi%C3%B3rka-wojska-i-obrony.128630/) | SIM       | [Código no GitHub (v2)](https://github.com/rafsaf/scripts_tribal_wars/blob/2024-09-01/public/collect_troops_v2.js)     |
| outros servidores | -                                                                                                                                                                    | NÃO       | [Código no GitHub (v2.3)](https://github.com/rafsaf/scripts_tribal_wars/blob/2025-09-22/public/collect_troops_v2.3.js) |

!!! warning

    O uso em outras versões de idioma do jogo **onde o roteiro não é permitido** pelo suporte pode resultar na suspensão da conta. Use por sua conta e risco.

=== "tribalwars.net"

    ```title="Roteiro de Coleta de Exército e Defesa"
    --8<-- "army_script_tribalwars_net_en.txt"
    ```

=== "plemiona.pl"

    ```title="Roteiro de Coleta de Exército e Defesa"
    --8<-- "army_script_plemiona_pl_en.txt"
    ```

=== "outros servidores"

    ```title="Roteiro de Coleta de Exército e Defesa"
    --8<-- "army_script_latest.txt"
    ```

## Instalação

A instalação é idêntica à de todos os roteiros para a barra de acesso rápido; você precisa colar o conteúdo em um roteiro recém-criado na barra de acesso rápido do jogo.

## Instruções de Uso

1. Crie um roteiro para a barra de acesso rápido e clique nele
2. Aguarde o resultado
3. Vá para o plano selecionado
4. Cole os dados e confirme

![Exemplo de saída do roteiro](image-2.png)

## Descrição

Após clicar, um "contador" com o progresso aparece no meio da tela, e em seguida o resultado em uma janela. Funciona tanto nas abas de Exército quanto de Defesa. As configurações padrão para cópia têm o cache definido como verdadeiro e o tempo de cache como 5 minutos. Durante esse tempo, o roteiro exibe o resultado salvo no navegador em vez de percorrer todos os membros e coletar os dados novamente. Em caso de dúvida se estamos lidando com um resultado novo ou antigo, a data da coleta aparece na parte inferior.

Os dados gerados pela execução do roteiro devem ser colados no plano no site.

Opções:

A configuração ocorre usando o objeto **COLLECT_TROOPS_DATA_V2**. Note que cada parâmetro É OPCIONAL. Se ambas as variáveis não forem definidas ou forem definidas, mas não houver chaves, serão usados padrões sensatos.

- **cache**: <boolean> (padrão: `true`) é responsável por armazenar o resultado no navegador para não clicar acidentalmente várias vezes seguidas e sobrecarregar os servidores do jogo. Definir `cache: false` faz com que o resultado não seja armazenado (por exemplo, quando pretendemos coletar dados de duas tribos, pulando imediatamente para a outra). Note que se a tribo tiver um número enorme de aldeias, pode ocupar muito espaço no localStorage (~máx 5MB). Por causa disso, o limite é de 1MB; se a saída for > 1MB, o salvamento no localStorage será ignorado.

- **cacheTime**: <number> (padrão: `5`) é o tempo de armazenamento do resultado no navegador, em minutos.

- **removedPlayers**: <string> (padrão: `""`) aqui inserimos os apelidos dos jogadores dos quais não queremos coletar informações de tropas, separando com ponto e vírgula como nas mensagens do jogo, por exemplo, "Rafsaf;kmic;alguem"

- **allowedPlayers**: <string> (padrão: `""`) aqui inserimos os apelidos dos jogadores dos quais SOMENTE! (se estiver vazio, todos os jogadores da tribo serão usados) queremos coletar informações de tropas, separando com ponto e vírgula como nas mensagens do jogo, por exemplo, "Rafsaf;kmic;alguem"

- **language**: <string> (padrão: `"pl"`) deve ser `"en"` ou `"pl"`. Se algo diferente for usado, o roteiro usará o inglês.

- **showNicknamesTroops**: <boolean> (padrão: `false`) quando definido como verdadeiro, faz com que o apelido do jogador apareça no início de cada linha. Aplica-se apenas na aba Tropas, semelhante a `showNicknamesDeff`.

- **showFirstLineTroops**: <boolean> (padrão: `false`) quando definido como verdadeiro, adiciona uma linha extra no topo do resultado, especificada pela variável `firstLineDeff`. Aplica-se apenas na aba Tropas, semelhante a `showFirstLineDeff`.

- **firstLineTroops**: <string> (padrão: `""`) linha que será mostrada no topo do resultado quando `showFirstLineTroops` for verdadeiro. Aplica-se apenas na aba Tropas, semelhante a `showNicknamesDeff`.

- **showNicknamesDeff**: <boolean> (padrão: `false`) quando definido como verdadeiro, faz com que o apelido do jogador apareça no início de cada linha. Aplica-se apenas na aba Defesa, semelhante a `showNicknamesTroops`.

- **showFirstLineDeff**: <boolean> (padrão: `false`) quando definido como verdadeiro, adiciona uma linha extra no topo do resultado, especificada pela variável `firstLineDeff`. Aplica-se apenas na aba Defesa, semelhante a `showFirstLineTroops`.

- **firstLineDeff**: <string> (padrão: `""`) linha que será mostrada no topo do resultado quando `showFirstLineTroops` for verdadeiro. Aplica-se apenas na aba Defesa, semelhante a `firstLineTroops`.
