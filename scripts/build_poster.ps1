$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
Push-Location $taskRoot
try {
    New-Item -ItemType Directory -Force -Path 'output/pdf', 'tmp/tex-cache', 'tmp/pdfs/latex' | Out-Null
    $env:TEXMFVAR = Join-Path $taskRoot 'tmp/tex-cache'
    for ($taskPass = 1; $taskPass -le 2; $taskPass++) {
        & xelatex --disable-installer --interaction=nonstopmode --halt-on-error --output-directory=tmp/pdfs/latex --jobname=RACE_poster_A0_portrait posterv.tex
        if ($LASTEXITCODE -ne 0) { throw "XeLaTeX failed on pass $taskPass" }
    }
    Copy-Item -LiteralPath 'tmp/pdfs/latex/RACE_poster_A0_portrait.pdf' -Destination 'output/pdf/RACE_poster_A0_portrait.pdf' -Force
    & pdftoppm -f 1 -singlefile -scale-to 3200 -png output/pdf/RACE_poster_A0_portrait.pdf output/pdf/RACE_poster_A0_portrait
    if ($LASTEXITCODE -ne 0) { throw 'Poster preview rendering failed' }
} finally {
    Pop-Location
}
