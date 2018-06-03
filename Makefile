.PHONY: all

all : README.md cv.html cv.pdf cv.odt cv.jats cv.tex # cv_html.pdf

cvproc.md : cv.md reffilter.py
	python reffilter.py < cv.md > cvproc.md

README.md : cvproc.md
	pandoc cvproc.md --to gfm > README.md

# https://devilgate.org/blog/2012/07/02/tip-using-pandoc-to-create-truly-standalone-html-files/
cv.html : cvproc.md cv.css
	pandoc cvproc.md --to html -s -H cv.css > cv.html

cv.pdf : cv.tex
	latexmk -pdf -g cv.tex

cv_html.pdf : cvproc.md cv_pdf.css
	pandoc cvproc.md --to html -s -H cv_pdf.css -o cv_html.pdf

cv.tex : cvproc.md cvpreamble.tex
	pandoc cvproc.md --to latex -s -H cvpreamble.tex -o cv.tex
	sed -i '/^\\begin{longtable}/i\{\\rowcolors{1}{white}{white!70!black!30}' cv.tex
	sed -i '/^\\end{longtable}/a\}' cv.tex
	sed -i '/^\\toprule$$/d' cv.tex
	sed -i '/^\\midrule$$/d' cv.tex
	sed -i '/^\\bottomrule$$/d' cv.tex
	sed -i '/^\\endhead$$/d' cv.tex
	sed -i '/^\\usepackage{xcolor}$$/c\\\usepackage[table]{xcolor}' cv.tex

cv.odt : cvproc.md
	pandoc cvproc.md --to odt -o cv.odt

cv.jats : cvproc.md
	pandoc cvproc.md --to jats -o cv.jats
