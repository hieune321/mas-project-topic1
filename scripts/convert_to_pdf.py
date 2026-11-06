import sys
from pathlib import Path
import win32com.client
import shutil

# Make sure official docx exists
src_docx = Path("outputs/reports/Computer_Project_Topic_1_Report.docx").resolve()
official_docx = Path("outputs/reports/MAS291_Nhom1_BaoCao_ComputerProject_DeTai1.docx").resolve()
shutil.copyfile(src_docx, official_docx)
print("Copied to official docx:", official_docx)

pdf_path1 = src_docx.with_suffix(".pdf")
pdf_path2 = official_docx.with_suffix(".pdf")

word = None
try:
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    print("Converting", src_docx.name, "to PDF...")
    doc1 = word.Documents.Open(str(src_docx), ReadOnly=1)
    doc1.SaveAs(str(pdf_path1), FileFormat=17)
    doc1.Close(False)
    print("Exported:", pdf_path1)

    print("Converting", official_docx.name, "to PDF...")
    doc2 = word.Documents.Open(str(official_docx), ReadOnly=1)
    doc2.SaveAs(str(pdf_path2), FileFormat=17)
    doc2.Close(False)
    print("Exported:", pdf_path2)

except Exception as e:
    print("Error during Word COM conversion:", e)
    sys.exit(1)
finally:
    if word:
        try:
            word.Quit()
        except Exception:
            pass

print("PDF generation completed successfully!")
