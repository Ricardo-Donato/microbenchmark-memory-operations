 **ANÁLISE COMPARATIVA DE DESEMPENHO OPERACIONAL: WINDOWS VS. LINUX EM AMBIENTES DE CIDADES INTELIGENTES1**

**Gabriel Possani2, Henrique Tonel3 e Pedro Donato4**

1 Projeto baseado em PBL desenvolvido na Unijuí; trabalho da disciplina Programação para Ciência de Dados.  
2 Estudante do curso de Engenharia de Software.  
3 Estudante do curso de Engenharia de Software.  
4 Estudante do curso de Ciência da Computação.

**INTRODUÇÃO**  
Uma empresa responsável pela integração de serviços digitais em cidades inteligentes precisa comparar o tempo das operações de Windows e Linux. Em vista disso, nossa equipe foi contratada para realizar um levantamento de análise para apresentar dados concretos em condições de ambiente equivalentes, a fim de realizar uma recomendação para a empresa decidir entre qual sistema operacional escolher baseado naquele que teve melhor desempenho nas operações de alocação, escrita, leitura e liberação de memória. Cabe ressaltar que a eficiência do sistema operacional é crítica para cenários de cidades inteligentes, onde o processamento de grandes volumes de dados exige baixa latência e alta disponibilidade.

**METODOLOGIA**  
Para garantir a equivalência dos ambientes na configuração experimental, os testes foram conduzidos na modalidade de dual boot no mesmo computador. Tal escolha se pelo dual boot garantir que o hardware físico (processador, memória ram e armazenamento) seja exatamente o mesmo nos dois sistemas operacionais, eliminando a variação introduzida por virtualização (overhead de hypervisor, alocação de vCPUs/RAM). Isso aproxima as condições experimentais dos dois ambientes, permitindo atribuir eventuais diferenças de desempenho ao sistema operacional, e não ao hardware.  
Nisso, temos como identificação do ambiente a versão Windows 11 e a distribuição Ubuntu 26.04 LTS (Resolute Raccoon) para Linux, além de que ambos utilizam arquitetura x64, 16 GB de RAM e a versão do Python é 3.14.8. Em outras palavras, a escolha das versões priorizou a mais recente de Windows, Linux (Ubuntu nesse caso) e Python.  
Com relação ao hardware físico, as configurações abrangem o processador Intel Core i5-10210U (10ª geração, 1.6 GHz), memória RAM de 16 GB, HD de 1 TB (configuração de fábrica) e o modelo de notebook Samsung Book X40 (np550xcj).  
Vale ressaltar que para as variáveis de experimento foram definidas no âmbito independente (sistema operacional, isto é, Windows ou Linux), dependente (tempo de alocação, escrita, leitura e liberação de memória (ms), para cada tamanho de bloco) e controladas. E àquelas controladas, deve ser exposto que não inclui somente o hardware, mas também o código-fonte do benchmark, a versão do python 3.14.8, os tamanhos de bloco (100 a 1000 MB), o número de repetições (100) e a ausência de outros programas em execução.

**RESULTADOS E DISCUSSÃO**  
Para avaliar o comportamento dos sistemas operacionais Windows 11 e Ubuntu 26.04 LTS em cenários voltados a cidades inteligentes, foram executadas 100 repetições de testes de microbenchmark variando blocos de dados de 100 MB a 1000 MB (em passos de 100 MB). As operações mensuradas contemplaram o ciclo completo de gerenciamento de memória: alocação, escrita, leitura e liberação.

Analisando o comportamento individual de cada etapa por meio dos gráficos coletados, a alocação de memória (alloc\_ms) para Windows 11 apresentou tempos médios de alocação inferiores aos do Ubuntu 26.04 LTS na maior parte do escopo, crescendo de forma escalonada até atingir um pico em torno de 900 MB (\~167 ms) e uma queda acentuada em 1000 MB (\~138,8 ms). Em contrapartida, o Linux demonstrou um comportamento estritamente linear e previsível em todas as grandezas de blocos, escalando proporcionalmente de 31,57 ms (100 MB) até 314,67 ms (1000 MB). Essa linearidade no Linux reflete uma alocação de páginas (*page allocation*) altamente determinística, ideal para ambientes de tempo real.

Com relação à escrita em memória (write\_ms), o Windows manteve latências menores para blocos de até 700 MB (por exemplo, \~155,9 ms em 500 MB contra 212,1 ms no Linux). Contudo, a partir de 800 MB e 900 MB, as curvas se cruzam e o Windows exibe oscilações de desempenho (queda para \~290,7 ms em 1000 MB), enquanto o Linux mantém um crescimento linear constante até 424,4 ms no bloco máximo.

Por outro lado, a etapa de leitura (read\_ms — verificação via hash MD5) representou a maior parcela do tempo total de execução. O Linux manteve um comportamento perfeitamente linear e estável do início ao fim (subindo de 126,1 ms em 100 MB para 1.241,5 ms em 1000 MB). Já o Windows apresentou um desempenho competitivo em blocos menores, mas sofreu instabilidades marcantes a partir de 700 MB, com picos de latência que chegaram a 1.445,8 ms no bloco de 900 MB, evidenciando maior variabilidade sob alta pressão de carga.

Quanto à liberação de memória (free\_ms)**,** a desalocação e coleta de lixo (*garbage collection*) mostraram tempos relativamente baixos para ambos os sistemas em blocos menores (abaixo de 10 ms para 100 MB). No entanto, o Windows registrou picos de maior sobrecarga na liberação de blocos intermediários e altos (atingindo média de 50,5 ms em 900 MB), ao passo que o Linux escalou de forma suave e controlada até 42,6 ms em 1000 MB.

Na visão global de desempenho, a partir da avaliação do tempo médio total acumulado de todas as operações (alocação \+ escrita \+ leitura \+ liberação) em todo o espectro de blocos, o Windows 11 registrou uma média global de 1.100,41 ms, enquanto o Ubuntu 26.04 LTS registrou 1.114,11 ms.

Embora os tempos globais brutos tenham ficado extremamente próximos (diferença inferior a 1,2% no acumulado), a análise qualitativa revela um aspecto crucial para ambientes de cidades inteligentes: o Linux demonstrou um comportamento altamente determinístico e linear, sem oscilações bruscas de latência. Em contrapartida, o Windows apresentou maior volatilidade e picos de instabilidade em blocos de grande volume. Em infraestruturas urbanas críticas — onde o processamento contínuo de fluxos de dados de tráfego, telemetria e sensores exige previsibilidade e baixa variação de resposta (*jitter*) —, a estabilidade estrutural do Linux torna-se um fator determinante para a tomada de decisão.

**CONSIDERAÇÕES FINAIS**  
Com base no que foi desenvolvido, o grupo conclui que a partir do levantamento de evidências feito é possível recomendar que a melhor opção de sistema operacional (SO) para escolha por parte da empresa seria o Linux/Windows. Isso se deve ao fato de que com a observância e análise persistente desde dados obtidos das mais diferentes grandezas de requisições, o SO Linux/Windows apresentou maior consistência e melhor desempenho em praticamente em todos os cenários apresentados graficamente no ambiente experimental equivalente.

**Palavras-chave**:  Cidades inteligentes. Desempenho operacional. Gerenciamento de memória. Linux. Windows. 

**REFERÊNCIAS BIBLIOGRÁFICAS**

**ESSAS SÃO REFERÊNCIAS DE EXEMPLO ABNT A SEREM SEGUIDAS:**  
**LIVRO:**  
PRODANOV, FREITAS, Cleber Cristiano, Ernani Cesar. Metodologia do Trabalho Científico: Métodos e Técnicas da Pesquisa e do Trabalho Acadêmico. 2\. ed. Novo Hamburgo: Editora Feevale, 2013\.  
**SITE:**  
Royal Society For Public Health. \#StatusOfMind: Social media and young people's mental health and wellbeing. Royal Society for Public Health, 2017\. Disponível em: https\://www\.rsph.org.uk/static/uploaded/d125b27c-0b62-41c5-a2c0155a8887cd01.pdf. Acesso em: 06 ago. 2024\. 