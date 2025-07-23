# AWS Toolbox - Guía en Español 🧰

Esta es una colección de scripts para automatizar tareas y gestionar infraestructura en AWS de forma segura y eficiente.

## 🚀 Configuración Inicial

### Requisitos
- Python 3.x
- AWS CLI configurado con SSO
- Ambiente virtual activado

### Instalación
```bash
# Crear ambiente virtual
python -m venv aws-toolbox-env

# Activar ambiente virtual (Windows)
.\aws-toolbox-env\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## 🔐 Configuración Multi-Cuenta

### Login en SSO
```bash
# Login en todas las sesiones SSO
aws sso login --profile AWSAdministratorAccess-3629XXXXXX23
aws sso login --profile Backend-Desarrollo-7712XXXXXX83
aws sso login --profile Backend-Produccion-6002XXXXXX00
# ... repetir para cada perfil
```

## 📊 Scripts de Consulta (Seguros - Solo Lectura)

### CloudWatch
| Script | Descripción | Comando |
|--------|-------------|---------|
| `cw_count_log_groups.py` | Cuenta grupos de logs | `python cloudwatch\cw_count_log_groups.py` |
| `cw_fetch_log_groups_with_creation_date.py` | Lista logs con fecha de creación | `python cloudwatch\cw_fetch_log_groups_with_creation_date.py` |

### EC2
| Script | Descripción | Comando |
|--------|-------------|---------|
| `ec2_find_unattached_volumes.py` | Encuentra volúmenes EBS no conectados | `python ec2\ec2_find_unattached_volumes.py` |
| Listar IPs elásticas no asignadas | Encuentra IPs que cuestan dinero | `aws ec2 describe-addresses --query "Addresses[?AssociationId==null]" --output table` |
| Listar instancias EC2 | Ver todas las instancias | `aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]" --output table` |

### S3
| Script | Descripción | Comando |
|--------|-------------|---------|
| Listar buckets | Ver todos los buckets S3 | `aws s3 ls` |
| `s3_list_old_files.py` | Lista archivos antiguos en S3 | `python s3\s3_list_old_files.py` |

## 💰 Scripts de Optimización de Costos

### ⚠️ IMPORTANTE: Estos scripts MODIFICAN recursos. Úsalos con cuidado.

| Script | Descripción | Riesgo | Ahorro Potencial |
|--------|-------------|--------|------------------|
| `ec2_delete_unattached_volumes.py` | Elimina volúmenes EBS no conectados | Medio | $10-500+/mes |
| `ec2_delete_unused_eips.py` | Elimina IPs elásticas no usadas | Bajo | $3.65/IP/mes |
| `cw_delete_log_groups.py` | Elimina logs antiguos | Medio | $5-100+/mes |
| `s3_delete_empty_buckets.py` | Elimina buckets S3 vacíos | Bajo | Mínimo |
| `ec2_delete_unused_amis.py` | Elimina AMIs no utilizadas | Alto | $5-50+/mes |

## 🔧 Scripts Multi-Cuenta

### Ejecutar en todas las cuentas
```bash
# Crear script para ejecutar en todas las cuentas
python multi_account_runner.py --script "cloudwatch\cw_count_log_groups.py"
```

## 📋 Casos de Uso Comunes

### 1. Auditoría de Costos (Seguro)
```bash
# Ver recursos que pueden estar costando dinero
python ec2\ec2_find_unattached_volumes.py
aws ec2 describe-addresses --query "Addresses[?AssociationId==null]" --output table
python cloudwatch\cw_count_log_groups.py
```

### 2. Inventario de Recursos
```bash
# Ver qué tienes en tu cuenta
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name,InstanceType]" --output table
aws s3 ls
python cloudwatch\cw_count_log_groups.py
```

### 3. Limpieza de Recursos (¡CUIDADO!)
```bash
# Solo después de confirmar que es seguro
python ec2\ec2_delete_unattached_volumes.py --dry-run
python ec2\ec2_delete_unused_eips.py --dry-run
```

## 🛡️ Mejores Prácticas de Seguridad

### Antes de ejecutar scripts de eliminación:
1. **Siempre usar `--dry-run`** primero
2. **Hacer backup** de recursos importantes
3. **Probar en cuenta de desarrollo** antes que producción
4. **Revisar logs** antes de confirmar eliminaciones
5. **Tener plan de rollback**

### Orden recomendado para nuevos usuarios:
1. Scripts de consulta (seguros)
2. Scripts con `--dry-run`
3. Scripts de eliminación en desarrollo
4. Scripts de eliminación en producción (con mucho cuidado)

## 🚨 Scripts por Nivel de Riesgo

### 🟢 Riesgo Bajo (Solo lectura)
- `cw_count_log_groups.py`
- `ec2_find_unattached_volumes.py`
- Comandos `aws describe-*`

### 🟡 Riesgo Medio (Modifican configuración)
- `cw_set_retention_policy.py`
- `iam_rotate_access_keys.py`

### 🔴 Riesgo Alto (Eliminan recursos)
- `ec2_delete_unattached_volumes.py`
- `ec2_delete_unused_amis.py`
- `cw_delete_log_groups.py`

## 💡 Tips para Ahorrar Dinero

### Recursos que comúnmente cuestan dinero innecesario:
1. **Volúmenes EBS no conectados** - $3-50+/mes cada uno
2. **IPs elásticas no asignadas** - $3.65/mes cada una
3. **Logs antiguos en CloudWatch** - $0.50/GB/mes
4. **AMIs no utilizadas** - $0.05/GB/mes por snapshots
5. **Instancias EC2 paradas** - Siguen cobrando por volúmenes EBS

### Comandos rápidos para auditoría:
```bash
# Ver costos potenciales
python ec2\ec2_find_unattached_volumes.py
aws ec2 describe-addresses --query "Addresses[?AssociationId==null].PublicIp" --output text
aws ec2 describe-instances --query "Reservations[*].Instances[?State.Name=='stopped'].[InstanceId,InstanceType]" --output table
```

## 🔄 Automatización

### Crear hooks para ejecutar automáticamente:
- Después de terminar instancias EC2
- Semanalmente para auditoría de costos
- Mensualmente para limpieza de logs antiguos

## 📞 Soporte

Si encuentras errores:
1. Verifica que tengas permisos suficientes
2. Confirma que el perfil AWS esté activo
3. Revisa que el servicio esté disponible en la región
4. Usa `--dry-run` para probar sin riesgo

## ⚖️ Licencia
MIT - Puedes usar, modificar y distribuir libremente.

---

**Recuerda**: Siempre probar en desarrollo antes que en producción. Estos scripts pueden ahorrar mucho dinero, pero úsalos con responsabilidad.