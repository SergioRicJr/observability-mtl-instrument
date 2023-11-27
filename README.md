## Descrição do projeto

O observability-mtl-instrument é um pacote que simplifica a instrumentação e configuração para coleta e envio de métricas, traces e logs. Por padrão a Stack utilizada é:
- Métricas: Prometheus e PushGateway
- Traces: Grafana/Tempo
- Logs: Grafana/Loki

## Tabela de conteúdos
* [Pacote de observabilidade](pacote-de-observabilidade)
* [Instalação](instalaçao)
* [Como usar](como-usar)
    - [Métricas](metricas)
    - [Traces](traces)
    - [Logs](logs)
* [Informações adicionais](informaçoes-adicionais)
    - [Métricas](metricas)
    - [Traces](traces)
    - [Logs](logs)
* [Próximas funcionalidades](proximas-funcionalidades)
* [Links](links)


## Pacote de observabilidade


## Instalação

Instale e atualize usando pip:

```bash
  pip install observability-mtl-instrument
```
    


## Como usar

### Métricas
#### importação da configuração de métricas:
```py
    from observability_mtl_instrument.metric_config import MetricConfig
```

#### Configuração básica para uso:

```py
    metric_config = MetricConfig(
        job_name='nome escolhido para a aplicação',
        prometheus_url='url do pushGateway para envio de métrica'
    )
```



#### Chamar métricas



## Informações adicionais

### Métricas:

#### Tipos de métrica
O prometheus possui diversos tipos de métrica, que podem ser conhecidas através de sua documentação, em https://prometheus.io/docs/concepts/metric_types. O projeto observability-mtl-instrument, trabalha com todas elas.

#### Métricas default
É possível adicionar e criar métricas de acordo com o seu objetivo, porém, a biblioteca já apresenta três métricas por padrão, são elas:
- http_requests_total_by_code 
    - 
    - Tipo: Counter
    - Labels: 
        - http_code: Código do status HTTP.
        - unmapped: True ou False, para dizer se a rota é ou não conhecida pela aplicação.
        - service: Nome do serviço, aplicação ou job.
- http_requests_duration_seconds
    - 
    - Tipo: Summary
    - Labels: 
        - url_path: Rota da requisição.
        - http_method: Método HTTP usado na requisição
        - unmapped: True ou False, para dizer se a rota é ou não conhecida pela aplicação.
        - service: Nome do serviço, aplicação ou job.
- requests_in_progress
    - 
    - Tipo: Gauge
    - Labels: 
        - service: Nome do serviço, aplicação ou job.