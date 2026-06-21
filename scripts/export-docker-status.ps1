param(
  [string]$SshTarget = "",
  [string]$PortalRoot = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
  $scriptDir = Split-Path -Parent $PSCommandPath
  return (Resolve-Path (Join-Path $scriptDir "..")).Path
}

function Convert-ToPublicService {
  param(
    [Parameter(Mandatory = $true)]$Container,
    [int]$Index
  )

  $name = [string]$Container.Names
  $lower = $name.ToLowerInvariant()
  $label = "Container $Index"
  $service = "rednet-container-$Index"
  $mode = "observe"
  $guard = "read-only status"
  $composeProject = "unset"
  $network = if ($Container.Networks) { "present" } else { "unset" }
  $volumes = if ($Container.Mounts) { "present" } else { "none" }
  $restartPolicy = "redacted"

  if ($lower -match "marcel|personal") {
    $label = "Personal assistant"
    $service = "rednet-personal-assistant"
    $mode = "assisted / observe"
    $guard = "isolated memory, no laboratory actions"
    $composeProject = "isolated"
  } elseif ($lower -match "science|coordinator|research") {
    $label = "Science coordinator"
    $service = "rednet-science-coordinator"
    $mode = "lab-coordinator / observe"
    $guard = "coordination without live commands"
    $composeProject = "template"
  } elseif ($lower -match "qwen|model|llm") {
    $label = "Model gateway"
    $service = "model-proxy-example"
    $mode = "private model gateway"
    $guard = "do not publish tokens/session/cookies"
    $composeProject = "private"
  } elseif ($lower -match "dashy|dashboard") {
    $label = "Service dashboard"
    $service = "rednet-dashboard"
    $mode = "read-only dashboard"
    $guard = "no control commands from portal"
  } elseif ($lower -match "homeassistant") {
    $label = "Home automation"
    $service = "rednet-home-automation"
    $mode = "external service"
    $guard = "do not mix with agent memory"
  } elseif ($lower -match "n8n") {
    $label = "Automation workflows"
    $service = "rednet-automation"
    $mode = "workflow service"
    $guard = "status only, no secrets"
  }

  $status = if ([string]$Container.State -eq "running") { "online" } else { [string]$Container.State }
  $endpoint = if ($Container.Ports) { "port redacted in public layer" } else { "internal" }

  [ordered]@{
    label = $label
    runtime = "docker"
    service = $service
    status = $status
    mode = $mode
    endpoint = $endpoint
    composeProject = $composeProject
    network = $network
    volumes = $volumes
    restartPolicy = $restartPolicy
    actionAllowed = $false
    guard = $guard
  }
}

$repoRoot = Get-RepoRoot
if (-not $PortalRoot) {
  $PortalRoot = Join-Path $repoRoot "portal"
}

$runtimeDir = Join-Path $PortalRoot "runtime"
$outputPath = Join-Path $runtimeDir "docker-status.local.js"

$dockerFormat = "{{json .}}"
$command = "docker ps -a --format '$dockerFormat'"

if ($SshTarget) {
  $raw = & ssh -o BatchMode=yes -o ConnectTimeout=8 $SshTarget $command
} else {
  $raw = & docker ps -a --format $dockerFormat
}

$services = @()
$index = 1
foreach ($line in $raw) {
  if (-not $line.Trim()) {
    continue
  }
  $container = $line | ConvertFrom-Json
  $services += Convert-ToPublicService -Container $container -Index $index
  $index += 1
}

$snapshot = [ordered]@{
  generatedAt = (Get-Date).ToString("o")
  mode = "read-only"
  source = $(if ($SshTarget) { "ssh" } else { "local" })
  services = $services
}

$json = $snapshot | ConvertTo-Json -Depth 8
$js = "window.REDNET_DOCKER_STATUS = $json;`n"

if ($DryRun) {
  Write-Host "[dry-run] docker services: $($services.Count)"
  Write-Host "[dry-run] output: $outputPath"
  exit 0
}

New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
Set-Content -LiteralPath $outputPath -Value $js -Encoding UTF8
Write-Host "Wrote $outputPath"
