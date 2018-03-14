.PHONY: all

all : README.md cv.html cv.pdf

README.md : cv.md
	pandoc cv.md --to gfm > README.md

cv.html : cv.md
	pandoc cv.md --to html -s > cv.html

cv.pdf : cv.md
	pandoc cv.md --to latex -o cv.pdf
