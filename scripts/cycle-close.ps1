[CmdletBinding()]
param(
  [switch]$Apply,
  [switch]$DryRun,
  [string]$RepoRoot = "",
  [string]$NasRoot = $env:REDNET_SKILLBOOK_NAS_ROOT,
  [string]$CommitMessage = "",
  [string]$Python = "python"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Apply -and $DryRun) {
  throw "Use either -Apply or -DryRun, not both."
}

$Mode = if ($Apply) { "Apply" } else { "DryRun" }
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
  $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
  $RepoRoot = Join-Path $scriptRoot ".."
}
$RepoRoot = (Resolve-Path $RepoRoot).Path
$ReportDir = Join-Path $RepoRoot "reports\cycles\$Timestamp"
$ReportPath = Join-Path $ReportDir "cycle-close-report.md"
$ArtifactsPath = Join-Path $ReportDir "artifacts-manifest.json"
$BackupDir = Join-Path $RepoRoot "backups\cycles\$Timestamp"
$ArchiveName = "rednet-airin-skillbook-$Timestamp.zip"
$ArchivePath = Join-Path $BackupDir $ArchiveName
$ArchiveHashPath = "$ArchivePath.sha256"
$StageDir = Join-Path $RepoRoot "tmp\cycle-close-stage-$Timestamp"
$SafeAddRoots = @(
  "README.md",
  "CHANGELOG.md",
  "AGENTS.md",
  "NEXT_START_HERE.md",
  ".gitignore",
  ".gitattributes",
  "assets",
  "docs",
  "skills",
  "packages",
  "protocols",
  "sensor-prototype",
  "scripts",
  "dist",
  "reports\cycles"
)

function Write-Info {
  param([string]$Message)
  Write-Host "[$Mode] $Message"
}

function Get-RepoRelativePath {
  param([Parameter(Mandatory=$true)][string]$Path)
  $full = (Resolve-Path $Path).Path
  if ($full.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
    return $full.Substring($RepoRoot.Length).TrimStart("\", "/")
  }
  return $full
}

function Redact-ReportText {
  param([AllowNull()][string]$Text)
  if ($null -eq $Text) {
    return ""
  }
  $value = [string]$Text
  $value = $value.Replace($RepoRoot, "<repo>")
  if ($env:USERPROFILE) {
    $value = $value.Replace($env:USERPROFILE, "<user-home>")
  }
  if ($env:LOCALAPPDATA) {
    $value = $value.Replace($env:LOCALAPPDATA, "<localappdata>")
  }
  $value = $value -replace "\\\\[A-Za-z0-9_.-]+\\[^\r\n ]+", "<unc-path>"
  $value = $value -replace "[A-Za-z]:\\Users\\[^\\\r\n ]+(\\[^\r\n ]*)?", "<local-path>"
  return $value
}

function Invoke-Git {
  param([Parameter(Mandatory=$true)][string[]]$Args)
  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    $output = & git -C $RepoRoot @Args 2>&1
    $code = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $oldPreference
  }
  if ($code -ne 0) {
    throw "git $($Args -join ' ') failed:`n$($output | Out-String)"
  }
  return (($output | Out-String).Trim())
}

function Invoke-Native {
  param(
    [Parameter(Mandatory=$true)][string]$Name,
    [Parameter(Mandatory=$true)][scriptblock]$Script
  )
  Write-Info $Name
  $stdoutFile = [System.IO.Path]::GetTempFileName()
  $stderrFile = [System.IO.Path]::GetTempFileName()
  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    & $Script > $stdoutFile 2> $stderrFile
    $code = $LASTEXITCODE
    $stdout = if (Test-Path $stdoutFile) { Get-Content -LiteralPath $stdoutFile -Raw -ErrorAction SilentlyContinue } else { "" }
    $stderr = if (Test-Path $stderrFile) { Get-Content -LiteralPath $stderrFile -Raw -ErrorAction SilentlyContinue } else { "" }
  } finally {
    $ErrorActionPreference = $oldPreference
    Remove-Item -LiteralPath $stdoutFile, $stderrFile -Force -ErrorAction SilentlyContinue
  }
  $combined = (($stdout, $stderr | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }) -join "`n").Trim()
  if ($code -ne 0) {
    throw "$Name failed:`n$combined"
  }
  if ([string]::IsNullOrWhiteSpace($combined)) {
    return "OK: $Name"
  }
  return "OK: $Name`n$combined"
}

function Get-PublicTextFiles {
  $roots = @("docs", "skills", "packages", "protocols", "sensor-prototype", "assets")
  $files = @()
  foreach ($root in $roots) {
    $path = Join-Path $RepoRoot $root
    if (Test-Path $path) {
      $files += Get-ChildItem -Path $path -Recurse -File -Force |
        Where-Object {
          $_.FullName -notmatch "\\(__pycache__|tmp|backups|private|runtime|secrets)\\" -and
          $_.Extension.ToLowerInvariant() -in @(".md", ".json", ".yaml", ".yml", ".ps1", ".py", ".txt", ".jsonl")
        }
    }
  }
  foreach ($rootFile in @("README.md", "CHANGELOG.md", "AGENTS.md", "NEXT_START_HERE.md", ".gitignore", ".gitattributes")) {
    $path = Join-Path $RepoRoot $rootFile
    if (Test-Path $path) {
      $files += Get-Item $path
    }
  }
  return $files | Sort-Object FullName -Unique
}

function Test-Utf8Files {
  Write-Info "Проверка UTF-8"
  $decoder = New-Object System.Text.UTF8Encoding($false, $true)
  foreach ($file in Get-PublicTextFiles) {
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    [void]$decoder.GetString($bytes)
  }
  return "OK: UTF-8 проверен"
}

function Test-Secrets {
  Write-Info "Secret scan"
  $patterns = @(
    "sk-[A-Za-z0-9_-]{20,}",
    "ghp_[A-Za-z0-9]{20,}",
    "github_pat_[A-Za-z0-9_]{20,}",
    "xox[baprs]-[A-Za-z0-9-]{20,}",
    "AKIA[0-9A-Z]{16}",
    "-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----",
    "(?i)access_token\s*[:=]\s*['""]?[A-Za-z0-9._-]{12,}",
    "(?i)api[_-]?key\s*[:=]\s*['""]?[A-Za-z0-9._-]{12,}",
    "(?i)password\s*[:=]\s*['""]?[^\s'""]{8,}"
  )
  foreach ($file in Get-PublicTextFiles) {
    $text = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    $rel = Get-RepoRelativePath $file.FullName
    Test-PublicTextForSensitiveMarkers -Text $text -Label $rel
    foreach ($pattern in $patterns) {
      if ([regex]::IsMatch($text, $pattern)) {
        throw "Possible secret pattern in $rel"
      }
    }
  }
  return "OK: секреты не найдены в публичных корнях"
}

function Test-PublicTextForSensitiveMarkers {
  param(
    [Parameter(Mandatory=$true)][string]$Text,
    [Parameter(Mandatory=$true)][string]$Label
  )
  $structuredKeys = @("payload", "message", "body", "content", "text", "token", "password", "session", "cookie")
  foreach ($key in $structuredKeys) {
    if ([regex]::IsMatch($Text, "(?i)""$key""\s*:")) {
      throw "Forbidden structured field '$key' in $Label"
    }
  }
  if ([regex]::IsMatch($Text, "(^|[\s'""=])\\\\[A-Za-z0-9_.-]+\\[^\r\n ]+")) {
    throw "Public file contains UNC-style path: $Label"
  }
  $privateIpPattern = "(?<!\d)(10\.(?:\d{1,3}\.){2}\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})(?!\d)"
  if ([regex]::IsMatch($Text, $privateIpPattern)) {
    throw "Public file contains private IPv4 address: $Label"
  }
}

function Test-Manifest {
  Write-Info "Проверка manifest"
  $manifestPath = Join-Path $RepoRoot "packages\hermes\rednet-airin-meta-skills\manifest.json"
  if (-not (Test-Path $manifestPath)) {
    throw "Manifest not found: $manifestPath"
  }
  $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($manifest.name -ne "rednet-airin-meta-skills") {
    throw "Unexpected manifest name: $($manifest.name)"
  }
  if (-not $manifest.skills -or $manifest.skills.Count -lt 1) {
    throw "Manifest has no skills"
  }
  foreach ($root in $manifest.includes.skill_roots) {
    $path = Join-Path $RepoRoot $root
    if (-not (Test-Path $path)) {
      throw "Manifest include path missing: $root"
    }
  }
  foreach ($skill in $manifest.skills) {
    $path = Join-Path $RepoRoot $skill.path
    if (-not (Test-Path $path)) {
      throw "Manifest skill path missing: $($skill.path)"
    }
    $skillFile = Join-Path $path "SKILL.md"
    if (-not (Test-Path $skillFile)) {
      throw "Manifest skill has no SKILL.md: $($skill.path)"
    }
  }
  return "OK: manifest содержит $($manifest.skills.Count) навыков"
}

function Test-ZipContents {
  Write-Info "Проверка ZIP"
  $zipPath = Join-Path $RepoRoot "dist\REDNET-AIRIN-META-SKILLS-2026-06-07.zip"
  if (-not (Test-Path $zipPath)) {
    throw "Release ZIP not found: $zipPath"
  }
  Add-Type -AssemblyName System.IO.Compression.FileSystem
  $archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
  try {
    $entries = $archive.Entries | ForEach-Object { $_.FullName -replace "\\", "/" }
  $required = @(
      "skills/rednet/rednet-double-evaluation/SKILL.md",
      "skills/rednet/rednet-neural-service-node/SKILL.md",
      "protocols/session-guided-activation.md",
      "sensor-prototype/airin-signal-sensor/sensor.py",
      "sensor-prototype/airin-neural-service-node/airin_neural_service_node.py",
      "packages/hermes/rednet-airin-meta-skills/manifest.json",
      "packages/hermes/rednet-airin-meta-skills/install.ps1"
    )
    foreach ($entry in $required) {
      if (-not ($entries | Where-Object { $_ -eq $entry -or $_.EndsWith("/$entry") })) {
        throw "ZIP missing required entry: $entry"
      }
    }
    $forbidden = $entries | Where-Object {
      $_ -match "(^|/)(\.env|raw|capsules|secrets|runtime|private)(/|$)" -or
      $_ -match "(^|/)(__pycache__|tmp|backups)(/|$)" -or
      $_ -match "\.(session|pem|p12|pfx|key|pyc)$"
    }
    if ($forbidden) {
      throw "ZIP contains forbidden entries: $($forbidden -join ', ')"
    }
    $textExtensions = @(".md", ".json", ".yaml", ".yml", ".ps1", ".py", ".txt", ".jsonl")
    foreach ($entry in $archive.Entries) {
      $entryName = $entry.FullName.ToLowerInvariant()
      $entryExt = [System.IO.Path]::GetExtension($entryName)
      if ($textExtensions -contains $entryExt) {
        $reader = New-Object System.IO.StreamReader($entry.Open(), [System.Text.Encoding]::UTF8)
        try {
          $text = $reader.ReadToEnd()
          Test-PublicTextForSensitiveMarkers -Text $text -Label "ZIP:$($entry.FullName)"
        } finally {
          $reader.Dispose()
        }
      }
    }
  } finally {
    $archive.Dispose()
  }
  return "OK: ZIP содержит обязательные файлы и не содержит запрещенные записи"
}

function Test-ShaFiles {
  Write-Info "Проверка SHA256"
  $shaFiles = Get-ChildItem -Path $RepoRoot -Recurse -File -Filter "*.zip.sha256" |
    Where-Object { $_.FullName -notmatch "\\(tmp|backups)\\" }
  foreach ($shaFile in $shaFiles) {
    $zipPath = $shaFile.FullName -replace "\.sha256$", ""
    if (-not (Test-Path $zipPath)) {
      throw "SHA file has no matching ZIP: $($shaFile.FullName)"
    }
    $expected = (Get-Content -LiteralPath $shaFile.FullName -Raw -Encoding UTF8).Trim().Split(" ")[0].ToUpperInvariant()
    $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $zipPath).Hash.ToUpperInvariant()
    if ($expected -ne $actual) {
      throw "SHA mismatch for $zipPath"
    }
  }
  return "OK: SHA256 проверен для $($shaFiles.Count) zip-архивов"
}

function Test-NasWritable {
  if (-not $Apply) {
    return "SKIP: NAS проверяется в Apply"
  }
  if ([string]::IsNullOrWhiteSpace($NasRoot)) {
    throw "Apply requires -NasRoot or REDNET_SKILLBOOK_NAS_ROOT"
  }
  Write-Info "Проверка NAS"
  New-Item -ItemType Directory -Path $NasRoot -Force | Out-Null
  return "OK: NAS доступен"
}

function Limit-ReportText {
  param([AllowNull()][string]$Text, [int]$MaxLines = 32)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return ""
  }
  $lines = ([string]$Text).Trim() -split "`r?`n"
  if ($lines.Count -le $MaxLines) {
    return ($lines -join "`n")
  }
  $shown = $lines | Select-Object -First $MaxLines
  return (($shown -join "`n") + "`n...`n[вывод сокращён: показано $MaxLines из $($lines.Count) строк]")
}

function Get-CheckTitle {
  param([AllowNull()][string]$Text)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return "Проверка без вывода"
  }
  $first = (([string]$Text) -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -First 1).Trim()
  if ($first.StartsWith("OK: ")) {
    return $first.Substring(4).Trim()
  }
  if ($first.StartsWith("SKIP: ")) {
    return $first.Substring(6).Trim()
  }
  if ($first.StartsWith("Git branch:")) {
    return "Git состояние"
  }
  if ([regex]::IsMatch($first, "(?i)^warning:")) {
    return "Предупреждения Git/формата"
  }
  if ($first.Length -gt 72) {

  }
  return $first
}

function Get-CheckIcon {
  param([AllowNull()][string]$Text)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return "✅"
  }
  if ([regex]::IsMatch($Text, "(?im)^SKIP:|\bSKIP\b|пропущ", "IgnoreCase")) {
    return "⏭️"
  }
  if ([regex]::IsMatch($Text, "(?im)warning:|предупреж", "IgnoreCase")) {
    return "⚠️"
  }
  return "✅"
}

function Get-CheckSummary {
  param([AllowNull()][string]$Text)
  if ([string]::IsNullOrWhiteSpace($Text)) {
    return "Команда завершилась успешно и не вернула дополнительный вывод."
  }
  $value = [string]$Text
  if ($value.StartsWith("Git branch:")) {
    if ([regex]::IsMatch($value, "\[ahead\s+(\d+)\]")) {
      return "Ветка чистая по рабочему дереву, есть локальные коммиты ahead origin."
    }
    return "Git-состояние зафиксировано в отчёте."
  }
  if ([regex]::IsMatch($value, "(?im)^OK:\s*(.+)$")) {
    $title = ([regex]::Match($value, "(?im)^OK:\s*(.+)$")).Groups[1].Value.Trim()
    if ([regex]::IsMatch($value, "(?s)Ran\s+\d+\s+tests?.*\bOK\b")) {
      $ran = [regex]::Match($value, "(?s)Ran\s+(\d+)\s+tests?")
      if ($ran.Success) {
        return "${title}: тесты прошли ($($ran.Groups[1].Value))."
      }
      return "${title}: тесты прошли."
    }
    if ([regex]::IsMatch($value, "(?im)warning:")) {
      return "${title}: успешно, но есть предупреждения формата/окончаний строк."
    }
    return "${title}: успешно."
  }

  if ([regex]::IsMatch($value, "(?im)^SKIP:\s*(.+)$")) {
    return ([regex]::Match($value, "(?im)^SKIP:\s*(.+)$")).Groups[1].Value.Trim()
  }
  return "Проверка завершилась успешно; подробности ниже."
}

function Format-ReportCheck {
  param(
    [Parameter(Mandatory=$true)][int]$Index,
    [AllowNull()][string]$Text
  )
  $value = if ($null -eq $Text) { "" } else { ([string]$Text).Trim() }
  $title = Get-CheckTitle -Text $value
  $icon = Get-CheckIcon -Text $value
  $summary = Get-CheckSummary -Text $value
  [string[]]$lines = @()
  if (-not [string]::IsNullOrWhiteSpace($value)) {
    $lines = [string[]]($value -split "`r?`n")
  }
  $details = ""
  if ($lines.Length -gt 1) {
    $details = ($lines | Select-Object -Skip 1) -join "`n"
  } elseif ($value.StartsWith("Git branch:")) {
    $details = $value.Substring("Git branch:".Length).Trim()
  }
  $details = Limit-ReportText -Text $details
  $block = "### $icon ${Index}. $title`n`nКоротко: $summary"

  if (-not [string]::IsNullOrWhiteSpace($details)) {
    $block += "`n`n~~~text`n$details`n~~~"
  }

  return $block
}

function New-CycleReport {
  param([string[]]$CheckResults, [string]$ArchiveHash = "", [string]$NasResult = "")
  $nasState = if (-not $Apply) {
    "dry-run-skip"
  } elseif ([string]::IsNullOrWhiteSpace($NasResult)) {
    "copy-pending"
  } else {
    "copy-created-sha-verified"
  }
  $safeCheckResults = @($CheckResults | ForEach-Object { Redact-ReportText $_ })
  $formattedChecks = @()
  for ($i = 0; $i -lt $safeCheckResults.Count; $i++) {
    $formattedChecks += Format-ReportCheck -Index ($i + 1) -Text $safeCheckResults[$i]
  }
  $checksBlock = $formattedChecks -join "`n`n"
  $modeIcon = if ($Apply) { "🚀" } else { "🧪" }
  $nasIcon = if ($nasState -eq "copy-created-sha-verified") { "✅" } elseif ($nasState -eq "dry-run-skip") { "⏭️" } else { "⏳" }
  $archiveHashText = if ([string]::IsNullOrWhiteSpace($ArchiveHash)) { "будет рассчитан в Apply" } else { $ArchiveHash }
  $body = @"
# 🧾 Отчёт закрытия цикла REDNET Skillbook

## 🧭 Сводка

- 🕒 Дата: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz")
- $modeIcon Режим: $Mode
- 📚 Репозиторий: REDNET-AIRIN-SKILLBOOK
- 🔁 Commit после закрытия: фиксируется итоговым выводом скрипта и GitHub origin
- $nasIcon NAS: $nasState

## ✅ Проверки

$checksBlock

## 📦 Артефакты

- 🗜️ Локальный архив: backups/cycles/$Timestamp/$ArchiveName
- 🔐 SHA256 архива: $archiveHashText
- 🗄️ NAS-копия: $nasState; путь не записывается в публичный отчёт

## 🛡️ Границы безопасности

- ✅ Live Hermes, Айрин, Алетия, VPN, Tailscale, Ubuntu, EdgeRouter и рабочие сессии не изменялись.
- ✅ Сырой чат, дневники, капсулы, OAuth/Telegram-сессии, токены, пароли и payload не включались.
"@
  if ($Apply) {
    New-Item -ItemType Directory -Path $ReportDir -Force | Out-Null
    Set-Content -LiteralPath $ReportPath -Value $body -Encoding UTF8
  }
  return $body
}

function New-ArtifactsManifest {
  param([string]$ArchiveHash)
  $distZip = Join-Path $RepoRoot "dist\REDNET-AIRIN-META-SKILLS-2026-06-07.zip"
  $doubleZip = Join-Path $RepoRoot "packages\rednet-double-evaluation-meta-skill-v1.3.0.zip"
  $items = @()
  foreach ($path in @($distZip, $doubleZip, $ArchivePath)) {
    if (Test-Path $path) {
      $items += [ordered]@{
        path = Get-RepoRelativePath $path
        sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
        bytes = (Get-Item -LiteralPath $path).Length
      }
    }
  }
  $manifest = [ordered]@{
    cycle_id = $Timestamp
    mode = $Mode
    public_repository = "REDNET-AIRIN-SKILLBOOK"
    nas_copy = "operator-configured"
    artifacts = $items
    forbidden = @("tokens", "oauth_sessions", "telegram_sessions", "raw_chat", "diary_capsules", "payload", "private_keys")
  }
  if ($Apply) {
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ArtifactsPath -Encoding UTF8
  }
}

function Add-SafeGitFiles {
  foreach ($root in $SafeAddRoots) {
    $path = Join-Path $RepoRoot $root
    if (Test-Path $path) {
      [void](Invoke-Git @("add", "--", $root))
    }
  }
}

function New-TrackedArchive {
  Write-Info "Создание локального архива"
  New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
  if (Test-Path $StageDir) {
    Remove-Item -LiteralPath $StageDir -Recurse -Force
  }
  New-Item -ItemType Directory -Path $StageDir -Force | Out-Null
  $files = (Invoke-Git @("ls-files", "--cached")) -split "`r?`n" | Where-Object { $_ }
  foreach ($rel in $files) {
    $src = Join-Path $RepoRoot $rel
    $dst = Join-Path $StageDir $rel
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Copy-Item -LiteralPath $src -Destination $dst -Force
  }
  if (Test-Path $ArchivePath) {
    Remove-Item -LiteralPath $ArchivePath -Force
  }
  Compress-Archive -Path (Join-Path $StageDir "*") -DestinationPath $ArchivePath -CompressionLevel Optimal
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $ArchivePath).Hash
  Set-Content -LiteralPath $ArchiveHashPath -Value "$hash  $ArchiveName" -Encoding ASCII
  Remove-Item -LiteralPath $StageDir -Recurse -Force
  return $hash
}

function Copy-ToNas {
  param([string]$ArchiveHash)
  Write-Info "Копирование на NAS"
  $target = Join-Path $NasRoot $Timestamp
  New-Item -ItemType Directory -Path $target -Force | Out-Null
  Copy-Item -LiteralPath $ArchivePath -Destination (Join-Path $target $ArchiveName) -Force
  Copy-Item -LiteralPath $ArchiveHashPath -Destination (Join-Path $target "$ArchiveName.sha256") -Force
  Copy-Item -LiteralPath $ReportPath -Destination (Join-Path $target "cycle-close-report.md") -Force
  $copiedHash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $target $ArchiveName)).Hash
  if ($copiedHash -ne $ArchiveHash) {
    throw "NAS SHA mismatch"
  }
  return "OK: NAS-копия создана и SHA совпадает"
}

function Commit-And-Push {
  Write-Info "Коммит и GitHub push"
  $branch = (Invoke-Git @("rev-parse", "--abbrev-ref", "HEAD")).Trim()
  $status = Invoke-Git @("status", "--porcelain")
  if ([string]::IsNullOrWhiteSpace($status)) {
    return (Invoke-Git @("rev-parse", "HEAD")).Trim()
  }
  if ([string]::IsNullOrWhiteSpace($CommitMessage)) {
    $CommitMessage = "Close REDNET Skillbook cycle $Timestamp"
  }
  [void](Invoke-Git @("commit", "-m", $CommitMessage))
  [void](Invoke-Git @("push", "origin", $branch))
  $localHead = (Invoke-Git @("rev-parse", "HEAD")).Trim()
  $remoteLine = (& git -C $RepoRoot ls-remote origin "refs/heads/$branch" 2>&1 | Out-String).Trim()
  if ($LASTEXITCODE -ne 0) {
    throw "git ls-remote failed:`n$remoteLine"
  }
  if (-not $remoteLine.StartsWith($localHead)) {
    throw "origin/$branch does not match local HEAD"
  }
  return $localHead
}

Push-Location $RepoRoot
try {
  if (-not (Test-Path (Join-Path $RepoRoot ".git"))) {
    throw "RepoRoot is not a git repository: $RepoRoot"
  }

  $checkResults = @()
  $checkResults += "Git branch: $(Invoke-Git @('status', '--short', '--branch'))"
  $checkResults += Invoke-Native "git diff --check" { git -C $RepoRoot diff --check }
  $checkResults += Invoke-Native "git diff --cached --check" { git -C $RepoRoot diff --cached --check }
  $checkResults += Test-Utf8Files
  $checkResults += Test-Secrets
  $checkResults += Test-Manifest
  $checkResults += Invoke-Native "REDNET schema/example validation" { & $Python (Join-Path $RepoRoot "scripts\validate-rednet-schemas.py") }
  $checkResults += Invoke-Native "Portal read-only validation" { & $Python (Join-Path $RepoRoot "scripts\validate-portal-readonly.py") }
  $checkResults += Invoke-Native "Hermes installer dry-run" { powershell -ExecutionPolicy Bypass -File (Join-Path $RepoRoot "packages\hermes\rednet-airin-meta-skills\install.ps1") -DryRun }
  $checkResults += Invoke-Native "Sensor unit tests" { & $Python -m unittest discover (Join-Path $RepoRoot "sensor-prototype\airin-signal-sensor\tests") }
  $checkResults += Invoke-Native "Wakefulness node unit tests" { & $Python -m unittest discover (Join-Path $RepoRoot "sensor-prototype\airin-wakefulness-node\tests") }
  $checkResults += Invoke-Native "Neural service node Stage 1 unit tests" { & $Python -m unittest discover (Join-Path $RepoRoot "sensor-prototype\airin-neural-service-node\tests") }
  $checkResults += Invoke-Native "Double evaluation package validator" { & $Python (Join-Path $RepoRoot "packages\rednet-double-evaluation-meta-skill\checks\validate_package.py") }
  $checkResults += Test-ZipContents
  $checkResults += Test-ShaFiles
  $checkResults += Test-NasWritable

  if (-not $Apply) {
    [void](New-CycleReport -CheckResults $checkResults)
    [void](New-ArtifactsManifest -ArchiveHash "")
    Write-Info "DryRun завершен. Для закрытия цикла запусти -Apply с настроенным NasRoot."
    exit 0
  }

  $reportPreview = New-CycleReport -CheckResults $checkResults
  Add-SafeGitFiles
  $archiveHash = New-TrackedArchive
  $nasResult = Copy-ToNas -ArchiveHash $archiveHash
  $checkResults += $nasResult
  $reportPreview = New-CycleReport -CheckResults $checkResults -ArchiveHash $archiveHash -NasResult $nasResult
  New-ArtifactsManifest -ArchiveHash $archiveHash
  Add-SafeGitFiles
  $head = Commit-And-Push
  $finalStatus = Invoke-Git @("status", "--short", "--branch")
  Write-Info "Цикл закрыт"
  Write-Host "HEAD: $head"
  Write-Host $finalStatus
} finally {
  Pop-Location
}
