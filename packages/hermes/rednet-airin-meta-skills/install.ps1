[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$DryRun,
    [string]$HermesHome,
    [string]$Profile,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

if (-not $Apply) {
    $DryRun = $true
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..\..\..")

if ($HermesHome) {
    $targetRoot = [System.IO.Path]::GetFullPath($HermesHome)
} elseif ($Profile) {
    $targetRoot = Join-Path $HOME (".hermes\profiles\" + $Profile)
} elseif ($env:LOCALAPPDATA) {
    $targetRoot = Join-Path $env:LOCALAPPDATA "hermes"
} else {
    $targetRoot = Join-Path $HOME ".hermes"
}

$skillRoots = @(
    @{ Source = "skills\rednet"; Target = "skills\rednet" },
    @{ Source = "skills\rednet-meta"; Target = "skills\rednet-meta" }
)

Write-Host "REDNET Airin meta-skills installer"
Write-Host "Mode: $(if ($Apply) { 'APPLY' } else { 'DRY-RUN' })"
Write-Host "Repository: $repoRoot"
Write-Host "Hermes target: $targetRoot"
Write-Host ""

foreach ($root in $skillRoots) {
    $sourceRoot = Join-Path $repoRoot $root.Source
    $targetBase = Join-Path $targetRoot $root.Target

    if (-not (Test-Path $sourceRoot)) {
        throw "Source skill root not found: $sourceRoot"
    }

    Get-ChildItem -LiteralPath $sourceRoot -Directory | ForEach-Object {
        $sourceSkill = $_.FullName
        $targetSkill = Join-Path $targetBase $_.Name

        Write-Host ("{0} -> {1}" -f $sourceSkill, $targetSkill)

        if ($DryRun) {
            return
        }

        if (Test-Path $targetSkill) {
            if ($Force) {
                $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
                $backupPath = "$targetSkill.backup-$stamp"
                Move-Item -LiteralPath $targetSkill -Destination $backupPath
                Write-Host "  existing skill moved to $backupPath"
            } else {
                Write-Host "  exists; skipped. Use -Force to backup and replace."
                return
            }
        }

        New-Item -ItemType Directory -Force -Path $targetBase | Out-Null
        Copy-Item -LiteralPath $sourceSkill -Destination $targetSkill -Recurse
        Write-Host "  installed"
    }
}

Write-Host ""
if ($DryRun) {
    Write-Host "Dry-run complete. Nothing was copied. Re-run with -Apply to install."
} else {
    Write-Host "Apply complete. Reload Hermes skills manually in a maintenance window."
}
