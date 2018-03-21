TEX_NAME = gintautas-cv-spark
INDUSTRY_NAME = gintautas-industry
ACADEMIC_NAME = gintautas-academic
ONEPAGE_NAME = gintautas-onepage
BIB_NAME = gintautas
PDF_NAME = gintautas

all:
	echo 'use `make academic` or `make industry`'

academic:
	cp -f ${ACADEMIC_NAME}.tex ${TEX_NAME}.tex
	make prespark
	python sparklines.py ${TEX_NAME}.tex
	make postspark

industry:
	cp -f ${INDUSTRY_NAME}.tex ${TEX_NAME}.tex
	make prespark
	python sparklines.py ${TEX_NAME}.tex
	make postspark

onepage:
	cp -f ${ONEPAGE_NAME}.tex ${TEX_NAME}.tex
	#bold my name in the bibliography without making it useless for other applications
	cat ${BIB_NAME}.bib | sed 's_V\. Gintautas_{\\bf V\. Gintautas}_' > ${BIB_NAME}_temp.bib
	python fill_contact.py
	xelatex ${TEX_NAME}.tex
	xelatex ${TEX_NAME}.tex
	#latex -interaction=batchmode  ${TEX_NAME}.tex
	#latex -interaction=batchmode  ${TEX_NAME}.tex
	#bibtex bibpublications
	bibtex bibselectedpublications
	#python sparklines.py ${TEX_NAME}.tex
	make postspark


prespark:
	#bold my name in the bibliography without making it useless for other applications
	cat ${BIB_NAME}.bib | sed 's_V\. Gintautas_{\\bf V\. Gintautas}_' > ${BIB_NAME}_temp.bib
	python fill_contact.py
	xelatex ${TEX_NAME}.tex
	xelatex ${TEX_NAME}.tex
	#latex -interaction=batchmode  ${TEX_NAME}.tex
	#latex -interaction=batchmode  ${TEX_NAME}.tex
	bibtex bibpublications
	bibtex bibinvitedtalks
	bibtex bibconferencepresentationsandproceedings

#spark:
#	cp -f ${TEACH_NAME}.tex ${TEX_NAME}.tex
#	make prespark
#	python sparklines.py
#	make postspark

postspark:
	xelatex -interaction=batchmode  ${TEX_NAME}.tex
	xelatex -interaction=batchmode  ${TEX_NAME}.tex
	#dvips -t letter -Ppdf ${TEX_NAME}.dvi -o ${TEX_NAME}.ps
	#ps2pdf ${TEX_NAME}.ps ${TEX_NAME}.pdf
	mv -f ${TEX_NAME}.pdf ${PDF_NAME}.pdf
	make clean
	open ${PDF_NAME}.pdf &


clean:
	rm -f ./sections/contact_information_filled.tex
	rm -f ./sections/*_spark.tex
	rm -f ${TEX_NAME}.tex
	rm -f ${TEX_NAME}.pdf
	rm -f ${TEX_NAME}.ps
	rm -f ${BIB_NAME}_temp.bib
	rm -f *.dvi
	rm -f *.log
	rm -f *.aux
	rm -f *.bbl
	rm -f *.blg
	rm -f *.out
	rm -f *.tcp
	rm -f *.tps
