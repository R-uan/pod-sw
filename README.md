# Desafio Tecnico Power of Data

### Dependencias
- `python311`
- `flask`
- `httpx`
- `functions-framework`

### API
- `/{recurso}`
- `/{recurso}?filtro=valor&filtro=valor...`
- `/{recurso}/{id}`
- `/{recurso}/{id}/{relação}`

#### Recursos, Relações e Filtros Disponiveis
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

