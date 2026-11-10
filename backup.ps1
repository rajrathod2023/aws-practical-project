$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot

try {
    New-Item -ItemType Directory -Force backups | Out-Null

    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
    $backupPath = "./backups/tasks-$timestamp.db"

    docker compose exec -T api python -c "import sqlite3; source = sqlite3.connect('file:/app/data/tasks.db?mode=ro', uri=True); target = sqlite3.connect('/tmp/tasks-backup.db'); source.backup(target); target.close(); source.close()"

    if ($LASTEXITCODE -ne 0) {
        throw "Database backup failed."
    }

    docker compose cp api:/tmp/tasks-backup.db $backupPath

    if ($LASTEXITCODE -ne 0) {
        throw "Copying the backup to your PC failed."
    }

    Write-Host "Backup saved: $backupPath"
}
finally {
    Pop-Location
}