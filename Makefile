default: output.pdf

doc.md:
	./scripts/merge_by_toc.py

output.pdf: doc.md
	./scripts/generate_pdf.sh
