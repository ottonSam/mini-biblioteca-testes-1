# Video de apresentação

https://drive.google.com/file/d/1JcxauWSH-Q1qgtHg96nBq1JfagD8h0rZ/view?usp=sharing

# Instruções de Execução

### 1. Criar o ambiente virtual (venv)

```bash
python3 -m venv .venv
```

### 2. Ativar o ambiente virtual

- **Linux / macOS:**

  ```bash
  source .venv/bin/activate
  ```

- **Windows:**
  ```cmd
  .venv\Scripts\activate
  ```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

_(ou: `pip install pytest pytest-cov coverage`)_

### 4. Rodar os testes

- **Executar todos os testes com pytest:**

  ```bash
  pytest -v
  ```

- **Executar testes com relatório de cobertura:**

  ```bash
  pytest --cov=biblioteca --cov-report=term-missing
  ```

- **Executar testes via unittest:**
  ```bash
  python -m unittest discover tests
  ```
