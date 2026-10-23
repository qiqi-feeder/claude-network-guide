# Read-only report. No tokens, subscription URLs, browser cookies or private configuration values.
$ErrorActionPreference = 'Stop'
$relatedNames = @('ANTHROPIC_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'ANTHROPIC_BASE_URL')
$environmentSummary = foreach ($scope in @('Process', 'User', 'Machine')) {
    foreach ($name in $relatedNames) {
        [pscustomobject]@{
            scope = $scope
            name = $name
            present = -not [string]::IsNullOrEmpty([Environment]::GetEnvironmentVariable($name, $scope))
        }
    }
}
$proxy = Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -ErrorAction SilentlyContinue
$routes = Get-NetRoute -ErrorAction SilentlyContinue
$report = [ordered]@{
    generated_at = (Get-Date).ToString('o')
    time_zone = (Get-TimeZone).Id
    system_proxy_enabled = [bool]$proxy.ProxyEnable
    proxy_points_to_loopback = [bool]($proxy.ProxyServer -match '(^|[=;])(?:127\.0\.0\.1|localhost):')
    proxy_processes = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match 'clash|verge|mihomo|sing-box' } | ForEach-Object { $_.ProcessName } | Sort-Object -Unique)
    up_interfaces = @(Get-NetAdapter -ErrorAction SilentlyContinue | Where-Object Status -eq 'Up' | Select-Object Name, InterfaceDescription)
    default_routes = @($routes | Where-Object DestinationPrefix -in @('0.0.0.0/0', '0.0.0.0/1', '128.0.0.0/1', '::/0', '::/1', '8000::/1') | Select-Object InterfaceAlias, DestinationPrefix, RouteMetric)
    public_ipv6_present = [bool](@(Get-NetIPAddress -AddressFamily IPv6 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -match '^[23]' -and $_.AddressState -eq 'Preferred' }).Count)
    related_environment_presence = @($environmentSummary)
    limitation = 'Read-only summary; routes and process names do not prove absence of leaks. No endpoint tests performed.'
}
$report | ConvertTo-Json -Depth 6
