# CloudFormation

Aquí se encontrarán las plantillas *CloudFormation* que se usarán para crear las pilas en AWS.

## Lo que está hecho

- `databases.yaml`:
  - Bucket donde meter los CSVs.
  - Lambda que se activa cuando se sube un archivo al bucket.
  - La tabla de DynamoDB.
- `network.yaml`:
  - VPC
  - 3 Subredes públicas con acceso a internet.
  - Grupo de seguridad para el balanceador de carga.
  - Grupo de seguridad para las tareas.
  - ECR.
- `testinstance.yaml`:
  - Instancia que crea y sube el docker container.
- `cluster.yaml`:
  - Cluster ECS que contiene las instancias que ejecutan el docker container.
