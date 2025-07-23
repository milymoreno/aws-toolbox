#!/usr/bin/env python3
"""
Script para ejecutar comandos AWS en múltiples perfiles/cuentas
Autor: Asistente Kiro
Licencia: MIT
"""

import boto3
import subprocess
import sys
import os
from typing import List, Dict

# Lista de todos tus perfiles AWS
PROFILES = [
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
]

def run_script_for_profile(script_path: str, profile: str) -> Dict:
    """
    Ejecuta un script Python para un perfil específico
    """
    print(f"\n{'='*60}")
    print(f"🔍 EJECUTANDO EN: {profile}")
    print(f"{'='*60}")
    
    # Configurar variable de entorno
    env = os.environ.copy()
    env['AWS_PROFILE'] = profile
    
    try:
        # Ejecutar el script
        result = subprocess.run(
            [sys.executable, script_path],
            env=env,
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos timeout
        )
        
        if result.returncode == 0:
            print(f"✅ ÉXITO en {profile}")
            if result.stdout.strip():
                print(f"📊 Resultado: {result.stdout.strip()}")
            return {
                'profile': profile,
                'status': 'success',
                'output': result.stdout.strip(),
                'error': None
            }
        else:
            print(f"❌ ERROR en {profile}")
            print(f"🚨 Error: {result.stderr.strip()}")
            return {
                'profile': profile,
                'status': 'error',
                'output': None,
                'error': result.stderr.strip()
            }
            
    except subprocess.TimeoutExpired:
        print(f"⏰ TIMEOUT en {profile}")
        return {
            'profile': profile,
            'status': 'timeout',
            'output': None,
            'error': 'Timeout después de 2 minutos'
        }
    except Exception as e:
        print(f"💥 EXCEPCIÓN en {profile}: {str(e)}")
        return {
            'profile': profile,
            'status': 'exception',
            'output': None,
            'error': str(e)
        }

def run_aws_command_for_profile(command: str, profile: str) -> Dict:
    """
    Ejecuta un comando AWS CLI para un perfil específico
    """
    print(f"\n{'='*60}")
    print(f"🔍 EJECUTANDO EN: {profile}")
    print(f"{'='*60}")
    
    try:
        # Construir comando completo
        full_command = f"aws --profile {profile} {command}"
        
        result = subprocess.run(
            full_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"✅ ÉXITO en {profile}")
            if result.stdout.strip():
                print(f"📊 Resultado: {result.stdout.strip()}")
            return {
                'profile': profile,
                'status': 'success',
                'output': result.stdout.strip(),
                'error': None
            }
        else:
            print(f"❌ ERROR en {profile}")
            print(f"🚨 Error: {result.stderr.strip()}")
            return {
                'profile': profile,
                'status': 'error',
                'output': None,
                'error': result.stderr.strip()
            }
            
    except Exception as e:
        print(f"💥 EXCEPCIÓN en {profile}: {str(e)}")
        return {
            'profile': profile,
            'status': 'exception',
            'output': None,
            'error': str(e)
        }

def print_summary(results: List[Dict]):
    """
    Imprime un resumen de todos los resultados
    """
    print(f"\n{'='*80}")
    print("📋 RESUMEN FINAL")
    print(f"{'='*80}")
    
    success_count = len([r for r in results if r['status'] == 'success'])
    error_count = len([r for r in results if r['status'] == 'error'])
    timeout_count = len([r for r in results if r['status'] == 'timeout'])
    exception_count = len([r for r in results if r['status'] == 'exception'])
    
    print(f"✅ Éxitos: {success_count}")
    print(f"❌ Errores: {error_count}")
    print(f"⏰ Timeouts: {timeout_count}")
    print(f"💥 Excepciones: {exception_count}")
    print(f"📊 Total: {len(results)}")
    
    # Mostrar resultados exitosos
    successful_results = [r for r in results if r['status'] == 'success' and r['output']]
    if successful_results:
        print(f"\n🎯 RESULTADOS EXITOSOS:")
        for result in successful_results:
            print(f"  • {result['profile']}: {result['output']}")
    
    # Mostrar errores
    failed_results = [r for r in results if r['status'] != 'success']
    if failed_results:
        print(f"\n🚨 CUENTAS CON PROBLEMAS:")
        for result in failed_results:
            print(f"  • {result['profile']}: {result['error']}")

def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python multi_account_runner.py --script <ruta_del_script>")
        print("  python multi_account_runner.py --aws-command '<comando_aws>'")
        print("\nEjemplos:")
        print("  python multi_account_runner.py --script cloudwatch\\cw_count_log_groups.py")
        print("  python multi_account_runner.py --aws-command 'ec2 describe-addresses --query \"Addresses[?AssociationId==null].PublicIp\" --output text'")
        sys.exit(1)
    
    mode = sys.argv[1]
    command_or_script = sys.argv[2]
    
    print(f"🚀 INICIANDO EJECUCIÓN EN {len(PROFILES)} CUENTAS")
    print(f"📝 Modo: {mode}")
    print(f"🎯 Comando/Script: {command_or_script}")
    
    results = []
    
    for profile in PROFILES:
        if mode == "--script":
            result = run_script_for_profile(command_or_script, profile)
        elif mode == "--aws-command":
            result = run_aws_command_for_profile(command_or_script, profile)
        else:
            print(f"❌ Modo desconocido: {mode}")
            sys.exit(1)
            
        results.append(result)
    
    print_summary(results)

if __name__ == "__main__":
    main()