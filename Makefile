.PHONY: all

all : README.md cv.html cv.pdf

cvproc.md : cv.md reffilter.py
	python reffilter.py < cv.md > cvproc.md

README.md : cvproc.md
	pandoc cvproc.md --to gfm > README.md

cv.html : cvproc.md
	pandoc cvproc.md --to html -s > cv.html

cv.pdf : cv.md
	pandoc cvproc.md --to latex -o cv.pdf
