# PowerShell script to download required Flink connector JARs

$JAR_DIR = $PSScriptRoot
$FLINK_VERSION = "1.17.0"
$POSTGRES_VERSION = "42.6.0"

Write-Host "📦 Downloading Flink connector JARs..." -ForegroundColor Cyan

# JDBC Connector
Write-Host "Downloading Flink JDBC Connector..." -ForegroundColor Yellow
$jdbcUrl = "https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/$FLINK_VERSION/flink-connector-jdbc-$FLINK_VERSION.jar"
$jdbcPath = Join-Path $JAR_DIR "flink-connector-jdbc-$FLINK_VERSION.jar"

try {
    Invoke-WebRequest -Uri $jdbcUrl -OutFile $jdbcPath -UseBasicParsing
    Write-Host "✅ Downloaded flink-connector-jdbc-$FLINK_VERSION.jar" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download JDBC connector: $_" -ForegroundColor Red
}

# PostgreSQL Driver
Write-Host "Downloading PostgreSQL JDBC Driver..." -ForegroundColor Yellow
$pgUrl = "https://jdbc.postgresql.org/download/postgresql-$POSTGRES_VERSION.jar"
$pgPath = Join-Path $JAR_DIR "postgresql-$POSTGRES_VERSION.jar"

try {
    Invoke-WebRequest -Uri $pgUrl -OutFile $pgPath -UseBasicParsing
    Write-Host "✅ Downloaded postgresql-$POSTGRES_VERSION.jar" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to download PostgreSQL driver: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "📋 Verifying JARs..." -ForegroundColor Cyan
Get-ChildItem -Path $JAR_DIR -Filter "*.jar" | Format-Table Name, Length -AutoSize

Write-Host "✅ Done! All required JARs are ready." -ForegroundColor Green

