from plmc_framework.architecture.view import TemplateParser

def indexView():
    return TemplateParser().render('index.html', data={})