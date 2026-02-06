# Desafio Técnico Power of Data

API wrapper para SWAPI (Star Wars API) deployada no Google Cloud com Functions e API Gateway.

## Dependências

`python3.11` • `flask` • `httpx` • `functions-framework` • `terraform` • `gcloud CLI`

## Estrutura

```
pod-sw/
├── src/
│   ├── main.py
│   ├── swapi.py
│   └── requirements.txt
├── terraform/
│   ├── main.tf
│   ├── openapi.yaml.tpl
│   └── credentials/
│       └── terraform-key.json    # ⚠️ Não versionar!
└── README.md
```

## Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements-dev.txt

# Executar API
functions-framework --target=star_wars_api --source=src/main.py

# Testes
pytest
```

## Deploy Google Cloud

### 1. Setup Projeto

```bash
cd terraform

# Autenticar
gcloud auth login

# Criar projeto
gcloud projects create pod-sw-api --name="Star Wars API Project"
gcloud config set project pod-sw-api

# Vincular billing (substitua BILLING_ACCOUNT_ID)
gcloud billing projects link pod-sw-api --billing-account=BILLING_ACCOUNT_ID

# Habilitar APIs
gcloud services enable cloudfunctions.googleapis.com \
  apigateway.googleapis.com \
  servicemanagement.googleapis.com \
  servicecontrol.googleapis.com \
  cloudbuild.googleapis.com \
  cloudresourcemanager.googleapis.com \
  run.googleapis.com
```

### 2. Service Account

```bash
# Criar service account
gcloud iam service-accounts create terraform-sa \
  --display-name="Terraform Service Account"

# Adicionar permissões
gcloud projects add-iam-policy-binding pod-sw-api \
  --member="serviceAccount:terraform-sa@pod-sw-api.iam.gserviceaccount.com" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding pod-sw-api \
  --member="serviceAccount:terraform-sa@pod-sw-api.iam.gserviceaccount.com" \
  --role="roles/iam.securityAdmin"

# Gerar chave (⚠️ manter segredo!)
gcloud iam service-accounts keys create credentials/terraform-key.json \
  --iam-account=terraform-sa@pod-sw-api.iam.gserviceaccount.com
```

### 3. Deploy com Terraform

```bash
terraform init
terraform plan
terraform apply    # Digite 'yes' para confirmar
```

### 4. Testar API

```bash
GATEWAY_URL=$(terraform output -raw gateway_url)

curl https://${GATEWAY_URL}/people
curl https://${GATEWAY_URL}/people/1
curl https://${GATEWAY_URL}/people/1/vehicles
curl "https://${GATEWAY_URL}/people?name=luke"
```

## Limpeza

```bash
terraform destroy
rm -rf .terraform terraform.tfstate* ../function.zip
```

## API Endpoints

**Padrões:**
- `/{recurso}` - Listar todos
- `/{recurso}?filtro=valor` - Filtrar
- `/{recurso}/{id}` - Buscar por ID
- `/{recurso}/{id}/{relação}` - Buscar relações

**Recursos:**

| Recurso | Relações | Filtros |
|---------|----------|---------|
| `people` | species, films, starships, vehicles | name, eye_color, gender, hair_color, skin_color |
| `planets` | residents, films | name, climate, terrain |
| `films` | characters, planets, species, starships, vehicles | title, director, producer, year |
| `starships` | films, pilots | name, model |
| `vehicles` | films, pilots | name, model, class |
| `species` | people, films | name, classification, eye_color, hair_color, designation |

## Infraestrutura

- Storage Bucket
- Cloud Function Gen 2
- API Gateway (API, Config, Gateway)
- IAM Bindings
