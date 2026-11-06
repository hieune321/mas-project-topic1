$docPath = "C:\Users\LENOVO\Downloads\mas-project\outputs\reports\MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.docx"
$pdfPath = "C:\Users\LENOVO\Downloads\mas-project\outputs\reports\MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.pdf"
$srcDocPath = "C:\Users\LENOVO\Downloads\mas-project\outputs\reports\Computer_Project_Topic_1_Report.docx"
$srcPdfPath = "C:\Users\LENOVO\Downloads\mas-project\outputs\reports\Computer_Project_Topic_1_Report.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false

try {
    Write-Host "Opening document $docPath ..."
    $doc = $word.Documents.Open($docPath)
    Write-Host "Exporting to $pdfPath ..."
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close([ref]0)
    Write-Host "Done MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.pdf"

    Write-Host "Opening document $srcDocPath ..."
    $doc2 = $word.Documents.Open($srcDocPath)
    Write-Host "Exporting to $srcPdfPath ..."
    $doc2.SaveAs([ref]$srcPdfPath, [ref]17)
    $doc2.Close([ref]0)
    Write-Host "Done Computer_Project_Topic_1_Report.pdf"
}
catch {
    Write-Error $_.Exception.Message
}
finally {
    $word.Quit([ref]0)
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}
