# Guia de Execução — memoria_benchmark.py

Script oficial do experimento, exigido pela ficha de pré-registro (itens 4 e 9). Testa blocos de 100 a 1000 MB, em passos de 100 MB, com 100 repetições para cada tamanho (1.000 testes no total). Mede separadamente o tempo de alocação, escrita, leitura e liberação de memória, em milissegundos, e gera um CSV com uma linha por teste.

## O que ele faz

Para cada tamanho de bloco (100, 200, 300, ..., 1000 MB) e para cada uma das 100 repetições daquele tamanho, o script:
1. aloca um bloco de memória do tamanho definido;
2. escreve dados nesse bloco;
3. lê o conteúdo do bloco (calculando um hash, para garantir que toda a memória seja efetivamente lida);
4. libera o bloco.

O tempo de cada uma dessas quatro operações é registrado em milissegundos e gravado em uma linha do arquivo CSV.

O mesmo script deve ser executado, sem nenhuma alteração, no Windows e no Linux (dual boot), para permitir a comparação entre os dois sistemas.

## Tempo esperado de execução

A execução completa (1.000 testes) deve levar entre 20 e 40 minutos, dependendo do hardware. Não interrompa a execução no meio: os dados só ficam completos ao final.

## Passo a passo (Windows ou Linux)

1. Coloque o arquivo `memoria_benchmark.py` na pasta do projeto (ex.: `Documents/benchmark` no Windows, ou `~/benchmark` no Linux).
2. Abra o terminal (PowerShell no Windows, terminal no Linux) dentro dessa pasta.
3. Rode o script:

   **Windows:**
```bash
   python memoria_benchmark.py --out resultados_windows.csv
```

   **Linux:**
```bash
   python3 memoria_benchmark.py --out resultados_linux.csv
```

4. Aguarde a finalização. O script imprime o progresso bloco a bloco (ex.: "bloco 300 mb concluído (100 testes em 28.4s)").
5. Ao final, confira se o arquivo CSV tem exatamente 1.000 linhas de dados (sem contar o cabeçalho): 10 tamanhos de bloco x 100 repetições.

## Parâmetros disponíveis

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `--out` | nome do arquivo csv de saída | `resultados.csv` |
| `--block-min` | menor tamanho de bloco, em mb | `100` |
| `--block-max` | maior tamanho de bloco, em mb | `1000` |
| `--block-step` | incremento entre tamanhos de bloco, em mb | `100` |
| `--repetitions` | número de repetições por tamanho de bloco | `100` |

Os quatro últimos parâmetros já vêm configurados conforme a ficha e não precisam ser alterados na execução oficial. Eles existem para permitir um teste rápido antes da execução completa, por exemplo:

```bash
python memoria_benchmark.py --block-min 10 --block-max 30 --block-step 10 --repetitions 3 --out teste.csv
```

Isso gera poucos registros em segundos, só para confirmar que o script está funcionando antes de rodar a versão completa (que demora mais).

## Sobre a identificação do sistema no CSV

O cabeçalho do csv (`bloco_MB,teste,alloc_ms,write_ms,read_ms,free_ms`) não tem uma coluna de sistema operacional, porque cada arquivo já é gerado por um sistema só (um csv no Windows, outro no Linux). O nome do arquivo (ex.: `resultados_windows.csv` / `resultados_linux.csv`) é quem identifica de qual sistema são os dados.

Na hora da análise (após coletar os dois arquivos), será necessário unir os dois csv em uma tabela só, adicionando uma coluna "sistema" (windows ou linux) para cada conjunto de linhas. Isso é feito na etapa de análise, não durante a coleta.

## Organização sugerida dos arquivos no repositório
