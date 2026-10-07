**Ficha de pré-registro experimental** 

**1\. Identificação do grupo** 

| Campo  | Preenchimento |
| ----- | ----- |
| Grupo | Equipe de Ciência de Dados |
| Integrantes | Gabriel Possani, Henrique Tonel e Pedro Donato |
| Responsável pelo  protocolo | Gabriel Possani |
| Responsável pela  execução | Gabriel Possani |
| Responsável pela  validação | Henrique Tonel |
| Responsável pelo GitHub | Pedro Donato |
| Endereço do repositório | [https://github.com/Ricardo-Donato/microbenchmark-memory-operations](https://github.com/Ricardo-Donato/microbenchmark-memory-operations) |
| Data | 17/09/2026 |

**2\. Pergunta norteadora**   
Em condições experimentais equivalentes, qual dos sistemas operacionais apresenta melhor desempenho nas operações de alocação, escrita, leitura e liberação de memória? 

**3\. Hipóteses**

1. Linux é mais rápido que Windows porque ele é modular.  
2. Tais resultados necessitam estar de acordo com o objetivo.  
3. O Linux tende a ter menor overhead nas chamadas de alocação/liberação de memória porque seu gerenciador de memória (glibc/malloc) é mais enxuto que o do Windows.  
4. O Windows pode apresentar maior variabilidade (menos previsibilidade) nos tempos de resposta devido a processos de background do sistema e do antivírus nativo.  
5. Para operações de leitura/escrita em blocos grandes de memória, a diferença entre os SOs tende a diminuir, já que o hardware passa a ser o fator limitante.

**4\. Requisitos fixos** 

| Elemento  | Requisito |
| ----- | ----- |
| Sistemas  | Windows e Linux |
| Operações  | Alocação, escrita, leitura e liberação |
| Ordem  | Alocar → escrever → ler → liberar |
| Blocos  | 100 a 1000 MB, com incremento de 100 MB |
| Repetições  | 100 para cada tamanho |
| Unidade  | Milissegundos |
| Formato  | CSV |
| Código  | Mesma versão nos dois sistemas |
| Execução  | Um ambiente de cada vez |

**5\. Configuração experimental** 

**Modalidade escolhida:**

Dual boot no mesmo computador 

**Justificativa da escolha:**   
Optamos por dual boot para garantir que o hardware físico (processador, memória ram e armazenamento) seja exatamente o mesmo nos dois sistemas operacionais, eliminando a variação introduzida por virtualização (overhead de hypervisor, alocação de vCPUs/RAM). Isso aproxima as condições experimentais dos dois ambientes, permitindo atribuir eventuais diferenças de desempenho ao sistema operacional, e não ao hardware.

**Identificação dos ambientes** 

| Item  | Windows  | Linux |
| ----- | ----- | ----- |
| Versão do sistema | Windows 10/11 (conferir versão instalada) | Distribuição escolhida (ex.: ubuntu 24.04) |
| Arquitetura | x64 | x64 |
| Versão do Python | Conferir com python--version | Conferir com python3--version |
| Memória disponível | 16 GB | 16 GB |
| Quantidade de vCPUs, se VM | \- | \- |
| RAM atribuída, se VM | \- | \- |
| Versão do VirtualBox, se VM | \- | \- |

**Hardware físico** 

| Item  | Configuração |
| ----- | ----- |
| Processador | Intel Core i5-10210U (10ª geração, 1.6 GHz) |
| Memória RAM | 16 GB |
| Armazenamento | HD 1 TB (configuração de fábrica) |
| Sistema hospedeiro, se VM | \- |
| Modelo do notebook | Samsung Book X40 (np550xcj) |

**6\. Variáveis do experimento** 

Classificação do que será alterado, o que será medido e o que deverá permanecer constante.

| Elemento  | Definição do grupo |
| ----- | ----- |
| Variável independente | Sistema operacional (Windows ou Linux) |
| Variáveis dependentes | Tempo de alocação, escrita, leitura e liberação de memória (ms), para cada tamanho de bloco |
| Variáveis controladas | Hardware físico (Samsung Book X40, i5-10210U, 16 GB RAM, HD 1 TB), código-fonte do benchmark, versão do python, tamanhos de bloco (100 a 1000 MB), número de repetições (100), ausência de outros programas em execução |

**7\. Condições mantidas constantes** 

Marquem e expliquem como cada condição será controlada: 

| Condição  | Controlada?  | Como será verificada? |
| ----- | ----- | ----- |
| Mesmo hardware físico  | \[x\] | Dual boot no mesmo Samsung Book X40 |
| Mesmo código  | \[x\] | Mesmo arquivo memory\_benchmark.py, versão única no github |
| Mesma versão do Python  | \[x\] | Conferir python \--version antes de cada execução |
| Mesmos blocos  | \[x\] | Script parametrizado de 100 a 1000 mb, incrementos de 100 mb |
| Mesmo número de repetições  | \[x\] | Script fixado em 100 repetições por tamanho de bloco |
| Aplicações desnecessárias fechadas | \[x\] | Fechar navegador, antivírus e demais programas antes da coleta |
| Somente um ambiente em execução | \[x\] | Dual boot garante que apenas um só roda por vez |

**8\. Ordem de execução** 

| Decisão  | Preenchimento |
| ----- | ----- |
| Primeiro sistema | Windows |
| Segundo sistema | Linux |
| Responsável pela  execução | Gabriel Possani |
| Data prevista | 26 e 27/09/2026 (sábado e domingo) |

A ordem deve ser registrada antes da coleta para impedir que seja modificada depois da observação dos resultados.

**9\. Arquivos produzidos** 

Cabeçalho sugerido:   
**bloco\_MB,teste,alloc\_ms,write\_ms,read\_ms,free\_ms** 

**10\. Regras de validação** 

| Verificação  | Regra |
| ----- | ----- |
| Quantidade de registros  | 1.000 registros por sistema |
| Tamanhos dos blocos  | 100, 200, ..., 1000 MB |
| Número dos testes  | 1 a 100 para cada bloco |
| Duplicidades  | Não repetir sistema \+ bloco \+ teste |
| Valores ausentes  | Nenhuma célula obrigatória vazia |
| Tipos  | Bloco e teste inteiros; tempos numéricos |
| Tempos  | Valores não negativos |
| Identificação  | Sistema correto em todos os registros |

**11\. Plano de análise** 

Os registros serão agrupados por **sistema operacional, tamanho do bloco de memória e operação medida.** 

Para cada grupo, serão calculados **média, mediana, desvio-padrão, mínimo e máximo dos tempos de alocação, escrita, leitura e liberação, em milissegundos.** 

Os resultados serão apresentados por meio de **tabelas comparativas e gráficos que relacionem tamanho do bloco e tempo, distinguindo Windows e Linux.** 

Consideraremos que um sistema teve melhor desempenho em uma operação e tamanho quando **apresentar menor medida central dos tempos, prioritariamente mediana e também média, considerando a variabilidade das 100 repetições.** 

Se os resultados forem diferentes entre operações ou tamanhos, **a conclusão será específica para cada caso e não afirmará superioridade geral de um sistema operacional.**

**12\. Aprovação** 

| Avaliação do professor  | Marcação |
| ----- | ----- |
| Aprovado para execução  | \[X\] |
| Aprovado com correções  | \[ \] |
| Necessita nova versão  | \[ \] |

**Correções solicitadas:**   
Nenhuma.
