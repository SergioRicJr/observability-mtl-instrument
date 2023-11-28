# Descrição do projeto

O observability-mtl-instrument é um pacote que simplifica a instrumentação e configuração para coleta e envio de métricas, traces e logs. Por padrão a Stack utilizada é:
- Métricas: Prometheus e PushGateway
- Traces: Grafana/Tempo
- Logs: Grafana/Loki

# Tabela de conteúdos
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


# Pacote de observabilidade
Para simplificar ainda mais o gerenciamento, armazenamento e visualizações de métricas, traces e logs, além de integração com a biblioteca é possível utilizar o pacote de observabilidade, que traz um docker-compose, diversas configurações e exemplos de uso para containers de Prometheus, Grafana/Loki, Grafana/Tempo, Grafana e NGINX. Está disponível em: "ver se posso adicionar link público" 

# Instalação

Instale e atualize usando pip:

```bash
  pip install observability-mtl-instrument
```
    


# Como usar

## Métricas
### importação da configuração de métricas:
```py
    from observability_mtl_instrument.metric_config import MetricConfig
```

### Configuração básica para uso:

```py
    metric_config = MetricConfig(
        job_name='nome escolhido para a aplicação',
        prometheus_url='url do pushGateway para envio de métrica'
    )
```



### Chamar métricas

```py
    metrics = metric_config.metrics

    # As métricas podem ser utilizadas em um middleware da aplicação para funcionar de forma a poluir menos o código 
    metrics['requests_in_progress'].labels(service='fastapi-app').inc()
```



# Informações adicionais

## Métricas:

### Tipos de métrica
O prometheus possui diversos tipos de métrica, que podem ser conhecidas através de sua documentação, em https://prometheus.io/docs/concepts/metric_types. O projeto observability-mtl-instrument, trabalha com todas elas.

### Métricas default
É possível adicionar e criar métricas de acordo com o seu objetivo, porém, a biblioteca já apresenta três métricas por padrão, são elas:
### http_requests_total_by_code:
Tipo: Counter
- Labels:
| Nome   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `http_code` | `string` | Código do status HTTP. |
| `unmapped` | `boolean` | True ou False, para dizer se a rota é ou não conhecida pela aplicação. |
| `service` | `string` | Nome do serviço, aplicação ou job. |

### http_requests_duration_seconds
Tipo: Summary
- Labels: 
| Nome   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `url_path` | `string` | Rota da requisição |
| `http_method` | `string` | Método HTTP usado na requisição |
| `unmapped` | `boolean` | True ou False, para dizer se a rota é ou não conhecida pela aplicação. |
| `service` | `string` | Nome do serviço, aplicação ou job. |

### requests_in_progress
Tipo: Gauge
- Labels: 
| Nome   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `service` | `string` | Nome do serviço, aplicação ou job. |


# Próximas funcionalidades

- Desenvolvimento de Middleware para Django Rest Framework ✏️🚧
- Desenvolvimento de Middleware para FastAPI ✏️🚧

# Links
- [PyPi releases (pendente)]()
- [Documentação ReadTheDocs](https://observability-mtl-instrument.readthedocs.io/pt-br/latest/)
- [Código fonte](https://github.com/SergioRicJr/observability-mtl-instrument)