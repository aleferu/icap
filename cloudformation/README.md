# CloudFormation

Aquí se encontrarán las plantillas *CloudFormation* que se usarán para crear las pilas en AWS.

## Lo que está hecho

- `network.yaml`:
  - VPC
  - 3 Subredes públicas con acceso a internet.
  - Grupo de seguridad para el balanceador de carga.
  - Grupo de seguridad para las tareas.
  - ECR.
  - Instancia que crea y sube el docker container.
- `databases.yaml`:
  - Bucket donde meter los CSVs.
  - Lambda que se activa cuando se sube un archivo al bucket.
