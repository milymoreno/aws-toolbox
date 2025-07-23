# Script para hacer login en todas las cuentas SSO
# Autor: Mildred Moreno desde Kiro

Write-Host "Iniciando login en todas las cuentas SSO..." -ForegroundColor Green

# Lista de todos los perfiles
$profiles = @(
    "AWSAdministratorAccess-3629XXXXXX23",
    "ActiveDirectory-9664XXXXXX41", 
    "Backend-Desarrollo-7712XXXXXX83",
    "Backend-Produccion-6002XXXXXX00",
    "Backend-UAT-3334XXXXXX28",
    "Connect-UAT-2254XXXXXX41",
    "DATALAKE_DEVOPS-8228XXXXXX89",
    "DATALAKE_DLLOV2-8087XXXXXX90",
    "DATALAKE_PRODV2-0975XXXXXX94",
    "Identity-UAT-9578XXXXXX74",
    "IdentityProduccion-4315XXXXXX10",
    "PublicacionesDMZ-1755XXXXXX73",
    "PuntosColombia-3629XXXXXX23",
    "SeguridadPerimetral-3882XXXXXX92",
    "serverless-datalake-framework-6480XXXXXX04",
    "SOC_PCO-1522XXXXXX19",
    "Transito-internet-2593XXXXXX09",
    "pco-admin-Web-Puntos-Colombia-3919XXXXXX37",
    "Admin-Puntos-Colombia-4643XXXXXX26",
    "Puntos-Ceiba-7063XXXXXX85",
    "UAT-Puntos-Colombia-6354XXXXXX92"
)

$successCount = 0
$errorCount = 0

foreach ($profile in $profiles) {
    Write-Host ""
    Write-Host "Procesando: $profile" -ForegroundColor Yellow
    
    try {
        aws sso login --profile $profile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Login exitoso: $profile" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "Error en login: $profile" -ForegroundColor Red
            $errorCount++
        }
    }
    catch {
        Write-Host "Excepcion en: $profile" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host ""
Write-Host "============================================"
Write-Host "RESUMEN FINAL" -ForegroundColor Cyan
Write-Host "============================================"
Write-Host "Logins exitosos: $successCount" -ForegroundColor Green
Write-Host "Logins fallidos: $errorCount" -ForegroundColor Red
Write-Host "Total procesados: $($profiles.Count)" -ForegroundColor Blue

if ($successCount -gt 0) {
    Write-Host ""
    Write-Host "Listo! Ahora puedes ejecutar scripts en multiples cuentas." -ForegroundColor Green
    Write-Host "Ejemplo: python multi_account_runner.py --script cloudwatch\cw_count_log_groups.py" -ForegroundColor Yellow
}