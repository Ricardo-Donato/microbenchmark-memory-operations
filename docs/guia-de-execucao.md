# GUIA DE EXECUÇÃO - `app_benchmark.py`

## O que este script faz
Simula o processamento de $N$ requisições de um app público (cenário: chatbot municipal). Cada requisição aloca, escreve, lê e libera um bloco de memória, representando o processo de integração descrito na situação-problema.

Enquanto a carga roda, o script monitora em segundo plano o uso de CPU, memória (do sistema e do próprio processo) e, quando disponível, a temperatura dos sensores do hardware.

Ao final, gera um relatório `.txt` com um resumo do hardware do dispositivo e os valores mínimo, médio e máximo de cada métrica coletada.

O **mesmo script** deve ser executado, sem nenhuma alteração, no Windows e no Linux (dual boot), para permitir a comparação entre os dois sistemas.

---

## Pré-requisitos
- Python 3.10 ou superior instalado.
- Biblioteca `psutil` instalada (instruções abaixo).

---

## Passo a passo - Windows

1. Coloque o arquivo `app_benchmark.py` em uma pasta de sua preferência (ex.: `C:\Users\SEU_USUARIO\Documents\benchmark`).
2. Abra o PowerShell dentro dessa pasta:
   - Na barra de endereços do Explorador de Arquivos, apague o texto, digite `powershell` e pressione **Enter**.
   - Ou segure `Shift`, clique com o botão direito num espaço vazio da pasta e escolha **Abrir janela do PowerShell aqui** (ou *Abrir no Terminal*).
3. Confirme que o arquivo está na pasta digitando:
   ```powershell
   dir
   ```
4. Instale a dependência:
   ```powershell
   pip install psutil
   ```
5. Rode o benchmark (exemplo com 1000 requisições):
   ```powershell
   python app_benchmark.py --requests 1000 --block-size 4 --out relatorio_windows.txt
   ```
6. Repita trocando `--requests` para `100` e para `10000`, sempre mudando o nome do arquivo em `--out` para não sobrescrever os relatórios anteriores (ex.: `relatorio_windows_100.txt`, `relatorio_windows_1000.txt`, `relatorio_windows_10000.txt`).

---

## Passo a passo - Linux (Ubuntu)

1. Coloque o arquivo `app_benchmark.py` em uma pasta de sua preferência (ex.: `~/benchmark`).
2. Abra o terminal dentro dessa pasta (clique com o botão direito na pasta, no gerenciador de arquivos, e procure a opção **Abrir no terminal**, ou navegue manualmente com `cd`).
3. Instale a dependência:
   ```bash
   pip install psutil
   ```
   *(Se der erro de permissão, use: `pip install psutil --user`)*
4. *(Opcional, mas recomendado)* Para o script conseguir ler a temperatura do hardware, instale e configure o `lm-sensors`:
   ```bash
   sudo apt install lm-sensors
   sudo sensors-detect
   ```
   *(Responda "yes" às perguntas padrão)*
5. Rode o benchmark (exemplo com 1000 requisições):
   ```bash
   python3 app_benchmark.py --requests 1000 --block-size 4 --out relatorio_linux.txt
   ```
6. Repita trocando `--requests` para `100` e para `10000`, sempre mudando o nome do arquivo em `--out` (ex.: `relatorio_linux_100.txt`, `relatorio_linux_1000.txt`, `relatorio_linux_10000.txt`).

---

## Parâmetros disponíveis

- `--requests`: Número de requisições simuladas. Aceita apenas `100`, `1000` ou `10000`.
- `--block-size`: Tamanho, em MB, do bloco de memória usado por requisição. Padrão: `4`.
- `--interval`: Intervalo, em segundos, entre cada amostra de monitoramento (cpu/memória/temperatura). Padrão: `0.2`.
- `--out`: Nome do arquivo de relatório `.txt` gerado ao final. Padrão: `relatorio.txt`.

---

## O que o relatório contém

- **Informações de hardware:** Sistema operacional, arquitetura, processador, núcleos físicos e lógicos, frequência da CPU, memória RAM total, memória swap total e discos (com espaço total, usado e livre).
- **Dados da execução:** Data/hora, número de requisições simuladas, tamanho do bloco usado e duração total da carga.
- **Uso de CPU (%):** Mínimo, médio e máximo durante a execução.
- **Uso de memória do sistema (% e MB):** Mínimo, médio e máximo.
- **Uso de memória do processo (RSS, em MB):** Mínimo, médio e máximo.
- **Temperaturas dos sensores (quando disponíveis):** Mínimo, médio e máximo por sensor. No Windows, geralmente aparece como "não disponível", pois o sistema não expõe essa informação sem software adicional.

---

## Organização sugerida dos arquivos no repositório

```text
resultados/
  relatorio_windows_100.txt
  relatorio_windows_1000.txt
  relatorio_windows_10000.txt
  relatorio_linux_100.txt
  relatorio_linux_1000.txt
  relatorio_linux_10000.txt
```

---

## Problemas comuns

- **`pip` não é reconhecido como comando:** Reinstale o Python marcando a opção **"Add Python to PATH"** durante a instalação.
- **`No matching distribution found for psutil`:** Confira se digitou o nome certo do pacote (`psutil`, com um L só).
- **`No such file or directory` ao rodar o python:** O terminal não está aberto na mesma pasta onde o arquivo `app_benchmark.py` foi salvo. Confirme com o comando `dir` (Windows) ou `ls` (Linux) antes de rodar.