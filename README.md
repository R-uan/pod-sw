# Desafio Tecnico Power of Data

### Dependencias
- `python311`
- `flask`
- `httpx`
- `functions-framework`
- `google cloud api` 
- `terraform`

## Estrutura do Projeto

```
pod-sw/
├── src/                          # Código da Cloud Function
│   ├── main.py
│   ├── swapi.py
│   └── requirements.txt
├── terraform/
│   ├── main.tf                   # Configuração principal do Terraform
│   ├── openapi.yaml.tpl          # Template do OpenAPI
│   ├── credentials/
│   │   └── terraform-key.json    # Credenciais (não versionar!)
│   └── terraform.tfstate         # Estado do Terraform (criado automaticamente)
└── README.md
```

## Google Cloud Setup

Execute estes comandos antes de rodar o Terraform:

```bash
# Login no Google Cloud
gcloud auth login

# Create project
gcloud projects create pod-sw-api --name="Star Wars API Project"

# Set as default project
gcloud config set project pod-sw-api

# Link billing account (required to use services)
# First, list your billing accounts
gcloud billing accounts list

# Link billing (replace BILLING_ACCOUNT_ID with actual ID from above)
gcloud billing projects link pod-sw-api --billing-account=BILLING_ACCOUNT_ID

# Habilitar APIs necessárias
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable run.googleapis.com

# Create service account for Terraform
gcloud iam service-accounts create terraform-sa \
  --display-name="Terraform Service Account"

# Grant Editor role
gcloud projects add-iam-policy-binding pod-sw-api \
  --member="serviceAccount:terraform-sa@pod-sw-api.iam.gserviceaccount.com" \
  --role="roles/editor"

gcloud projects add-iam-policy-binding pod-sw-api \
  --member="serviceAccount:terraform-sa@pod-sw-api.iam.gserviceaccount.com" \
  --role="roles/iam.securityAdmin"

# Create and download credentials
gcloud iam service-accounts keys create credentials/terraform-key.json \
  --iam-account=terraform-sa@pod-sw-api.iam.gserviceaccount.com
```

## Terraform Apply

### 1. Navegar para o diretório do Terraform

```bash
cd ./pod-sw/terraform
```

### 2. Inicializar o Terraform

```bash
terraform init
```

Este comando:
- Baixa os providers do Google Cloud
- Inicializa o backend local
- Prepara o diretório para uso

### 3. Visualizar o plano de execução

```bash
terraform plan
```

Este comando mostra o que será criado/modificado/destruído **sem aplicar mudanças**.

### 4. Aplicar as mudanças

```bash
terraform apply
```

- O Terraform mostrará o plano novamente
- Digite `yes` para confirmar
- Aguarde a criação dos recursos (~3-5 minutos)

### 5. Visualizar outputs

```bash
terraform output
```

### 6. Testar a API

```bash
# Obter a URL do gateway
GATEWAY_URL=$(terraform output -raw gateway_url)

# Testar endpoints
curl https://${GATEWAY_URL}/people
curl https://${GATEWAY_URL}/planets
curl https://${GATEWAY_URL}/films
curl https://${GATEWAY_URL}/people/1
curl https://${GATEWAY_URL}/people/1/vehicles
curl "https://${GATEWAY_URL}/people?name=luke"
```

## Limpeza

Para remover todos os recursos criados:

```bash
# Destruir infraestrutura
terraform destroy

# Opcional: remover arquivos de estado
rm -rf .terraform
rm terraform.tfstate*
rm ../function.zip
```

## Recursos Criados

Este Terraform cria:
- ✅ Storage Bucket (para código da função)
- ✅ Cloud Function Gen 2
- ✅ API Gateway API
- ✅ API Gateway Config
- ✅ API Gateway Gateway
- ✅ IAM Bindings (permissões)

## API Endpoints
- `/{recurso}`
- `/{recurso}?filtro=valor&filtro=valor...`
- `/{recurso}/{id}`
- `/{recurso}/{id}/{relação}`

### Recursos, Relações e Filtros Disponiveis
- `people`
    - Relações: species, films, starships, vehicles
    - Filtros: name, eye_color, gender, hair_color, skin_color
- `planets`
    - Relações: residents, films
    - Filtros: name, climate, terrain
- `films`
    - Relações: characters, planets, species, starships, vehicles
    - Filtros: title, director, producer, year
- `starships`
    - Relações: films, pilots
    - Filtros: name, model
- `vehicles`
    - Relações: films, pilots
    - Filtros: name, model, class
- `species`
    - Relações: people, films
    - Filtros: name, classification, eye_color, hair_color, designation

