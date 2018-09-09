compile:
	pip install --upgrade pip
	python setup.py install
	yes | pyinstaller showdownai.spec || mkdir -p $(dir $@)
	cp -r teams dist/showdownai/
	zip -r dist/showdownai-linux64.zip dist/showdownai/
	cd -- "$(dirname "$BASH_SOURCE")"
	pip install selenium
	pip install --upgrade numpy
	cp chromedriver /Users/labuser/anaconda3/bin

clean:
	rm -rf build dist
