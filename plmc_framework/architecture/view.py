from collections import deque
import re
from plmc_framework.helpers import get_absolute_path_of_frontend_file

class TemplateParser:
    """
        Class that is responsible for converting templates to actual HTML files.
    """

    _SUBSTITUTE_MARKER_REGEX = r'(\[~ var (.*) ~\])'
    _FOR_SUBSTITUTE_KEYWORD = 'forvar'
    _FOR_START_REGEX = r'\[~ for (.*) ~\]'
    _FOR_END_REGEX = r'\[~ endfor ~\]'

    def render(self, templatePath: str, data: dict) -> str:
        """
            Returns the final HTML of the given template substituted with given data.
            templatePath: Relative path (public_html being the root) of the template HTML file.
            data: Dictionary whose keys will be substituted with corresponding values in the template.

            Returns:
            Final HTML string.
        """

        absolutePath = get_absolute_path_of_frontend_file(templatePath)
        with open(absolutePath, 'r') as templateFile:
            return templateFile.read()
        
        """
        with open(absolutePath, 'r') as templateFile:
            fileContent = templateFile.read()
            substitutes = re.findall(TemplateParser._SUBSTITUTE_MARKER_REGEX, fileContent)
            processedContent = fileContent
            for fullSubstitute, substituteVariable in substitutes:
                suppliedData = data[substituteVariable]
                if f" {TemplateParser._FOR_SUBSTITUTE_KEYWORD} " in fullSubstitute:
                    suppliedData = substituteVariable

                processedContent = fileContent.replace(fullSubstitute, suppliedData)

            forStartStatementsIterator = re.finditer(TemplateParser._FOR_START_REGEX, fileContent)
            forStartsStatementsList = [(match.start(), match.group(1)) for match in forStartStatementsIterator]
            for index, forEndMatch in enumerate(re.finditer(TemplateParser._FOR_END_REGEX, fileContent)):
                startLineNo = processedContent.count('\n', 0, forStartsStatementsList[len(forStartsStatementsList) - index - 1][0])
                endLineNo = processedContent.count('\n', 0, forEndMatch.start())

                forLoopBody = "\n".join(processedContent.split('\n')[startLineNo + 1 : endLineNo])
                pumpedLoopBody = []

                exec(f'for {forStartsStatementsList[len(forStartsStatementsList) - index - 1][1]}:\n\tbody.append(forLoopBody)', {'body': pumpedLoopBody, 'forLoopBody': forLoopBody})
                
                splittedContent = processedContent.split('\n')
                for removeIndex in range(startLineNo, endLineNo + 1):
                    splittedContent.pop(removeIndex)
                for insertIndex in range(startLineNo, startLineNo + len(pumpedLoopBody)):
                    splittedContent.insert(insertIndex, pumpedLoopBody[insertIndex - startLineNo])

                processedContent = "\n".join(splittedContent)

            #print(processedContent)
            return processedContent
        """