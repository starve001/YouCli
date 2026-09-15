# Dot-source this file from your PowerShell profile:
#   . C:\path\to\Youcli\integrations\powershell.ps1

function Invoke-AiComplete {
    $line = Get-PSReadLineCurrentLine
    $cursor = Get-PSReadLineCursorPosition
    $result = & ai-complete --shell powershell --line $line --cursor $cursor
    if ($LASTEXITCODE -eq 0 -and $result) {
        [Microsoft.PowerShell.PSConsoleReadLine]::Replace(0, $line.Length, ($result -join "`n"))
    }
}

Set-PSReadLineKeyHandler -Chord 'Ctrl+G' -Function Invoke-AiComplete
