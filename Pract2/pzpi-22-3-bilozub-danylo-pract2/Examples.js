// Example 1

const vscode = require('vscode');
// Створюємо колекцію для діагностики
const diagnosticCollection = vscode.languages.createDiagnosticCollection('fileAnalyzer');
function activate(context) {
    // Реєструємо команду
    let disposable = vscode.commands.registerCommand('extension.analyzeFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor!');
            return;
        }
        const document = editor.document;
        const diagnostics = [];
        // Аналізуємо вміст файлу (приклад: пошук заборонених слів)
        const text = document.getText();
        const forbiddenWords = ['TODO', 'FIXME'];
        const lines = text.split('\n');
        lines.forEach((line, index) => {
            forbiddenWords.forEach(word => {
                const wordIndex = line.indexOf(word);
                if (wordIndex !== -1) {
                    const range = new vscode.Range(
                        index, wordIndex,
                        index, wordIndex + word.length
                    );
                    const diagnostic = new vscode.Diagnostic(
                        range,
                        `Found forbidden word: ${word}`,
                        vscode.DiagnosticSeverity.Warning
                    );
                    diagnostic.source = 'File Analyzer';
                    diagnostics.push(diagnostic);
                }
            });
        });
        // Оновлюємо діагностику
        diagnosticCollection.clear();
        diagnosticCollection.set(document.uri, diagnostics);
        // Показуємо повідомлення про результат
        vscode.window.showInformationMessage(`Analysis complete. Found ${diagnostics.length} issues.`);
    });
    // Реєструємо обробник зміни активного файлу
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(() => {
            diagnosticCollection.clear();
        })
    );
    // Додаємо команду до контексту
    context.subscriptions.push(disposable);
}
function deactivate() {
    diagnosticCollection.clear();
}
module.exports = {
    activate,
    deactivate
};



// Example 2

const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

function activate(context) {
    // Реєструємо команду для відкриття WebView
    context.subscriptions.push(
        vscode.commands.registerCommand('extension.showInteractiveWebView', () => {
            // Створюємо WebView-панель
            const panel = vscode.window.createWebviewPanel(
                'interactiveWebView',
                'Interactive WebView',
                vscode.ViewColumn.One,
                {
                    enableScripts: true // Дозволяємо JavaScript
                }
            );

            // Встановлюємо HTML-контент із вбудованими стилями та скриптами
            panel.webview.html = `
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
                    <title>Interactive WebView</title>
                </head>
                <body>
                    <h1>Text Analyzer</h1>
                    <textarea id="inputText" rows="5" cols="50" placeholder="Enter text to analyze..."></textarea>
                    <div>
                        <button onclick="analyzeText()">Analyze Text</button>
                        <button onclick="saveText()">Save to File</button>
                    </div>
                    <div id="result" style="margin-top: 20px;"></div>

                    <style>
                       
                    </style>

                    <script>
                        const vscode = acquireVsCodeApi();

                        function analyzeText() {
                            const text = document.getElementById('inputText').value;
                            vscode.postMessage({
                                command: 'analyzeText',
                                text: text
                            });
                        }

                        function saveText() {
                            const text = document.getElementById('inputText').value;
                            vscode.postMessage({
                                command: 'saveText',
                                text: text
                            });
                        }

                        window.addEventListener('message', event => {
                            const message = event.data;
                            const resultDiv = document.getElementById('result');
                            if (message.command === 'showResult') {
                                resultDiv.style.display = 'block';
                                resultDiv.innerHTML = '<strong>Result:</strong> ' + message.result;
                            }
                        });
                    </script>
                </body>
                </html>
            `;

            // Обробляємо повідомлення від WebView
            panel.webview.onDidReceiveMessage(
                async (message) => {
                    switch (message.command) {
                        case 'analyzeText':
                            // Аналізуємо текст: підраховуємо слова
                            const wordCount = message.text.trim().split(/\s+/).filter(word => word.length > 0).length;
                            const result = `Analysis completed: ${wordCount} word(s) detected.`;
                            // Надсилаємо результат назад до WebView
                            panel.webview.postMessage({
                                command: 'showResult',
                                result: result
                            });
                            break;
                        case 'saveText':
                            // Зберігаємо текст у файл
                            const workspaceFolders = vscode.workspace.workspaceFolders;
                            if (workspaceFolders) {
                                const filePath = path.join(workspaceFolders[0].uri.fsPath, 'webview_output.txt');
                                try {
                                    fs.writeFileSync(filePath, message.text);
                                    vscode.window.showInformationMessage(`Text saved to ${filePath}`);
                                } catch (err) {
                                    vscode.window.showErrorMessage(`Failed to save file: ${err.message}`);
                                }
                            } else {
                                vscode.window.showErrorMessage('No workspace open to save the file!');
                            }
                            break;
                    }
                },
                undefined,
                context.subscriptions
            );
        })
    );
}
function deactivate() {}
module.exports = {
    activate,
    deactivate
};




// Example 3

const vscode = require('vscode');
// Колекція для діагностики
const diagnosticCollectionn = vscode.languages.createDiagnosticCollection('mylangAnalyzer');
function activate(context) {
    // 1. Реєструємо провайдер автодоповнення для мови "mylang"
    const completionProvider = vscode.languages.registerCompletionItemProvider(
        'mylang',
        {
            provideCompletionItems(document, position) {
                // Отримуємо слово перед курсором
                const line = document.lineAt(position).text;
                const wordRange = document.getWordRangeAtPosition(position);
                const word = wordRange ? document.getText(wordRange) : '';

                // Список пропозицій
                const suggestions = [
                    {
                        label: 'function',
                        kind: vscode.CompletionItemKind.Keyword,
                        detail: 'Keyword to define a function',
                        documentation: 'Inserts a function declaration',
                        insertText: 'function '
                    },
                    {
                        label: 'print',
                        kind: vscode.CompletionItemKind.Function,
                        detail: 'Prints a message to the console',
                        insertText: 'print('
                    },
                    {
                        label: 'loop',
                        kind: vscode.CompletionItemKind.Keyword,
                        detail: 'Creates a loop structure',
                        insertText: 'loop {\n\t\n}',
                        range: wordRange
                    }
                ];
                // Фільтруємо пропозиції за введеним словом
                return suggestions.map(item => {
                    const completionItem = new vscode.CompletionItem(item.label, item.kind);
                    completionItem.detail = item.detail;
                    completionItem.documentation = item.documentation || item.detail;
                    completionItem.insertText = item.insertText;
                    if (item.range) {
                        completionItem.range = item.range;
                    }
                    return completionItem;
                });
            }
        },
        '' // Тригери для автодоповнення
    );
    // 2. Реєструємо команду для контекстного меню
    const uppercaseCommand = vscode.commands.registerCommand('mylang.convertToUppercase', () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor!');
            return;
        }
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection);
        if (!selectedText) {
            vscode.window.showWarningMessage('No text selected!');
            return;
        }
        // Перетворюємо виділений текст у верхній регістр
        editor.edit(editBuilder => {
            editBuilder.replace(selection, selectedText.toUpperCase());
        }).then(success => {
            if (success) {
                vscode.window.showInformationMessage('Text converted to uppercase!');
            } else {
                vscode.window.showErrorMessage('Failed to convert text.');
            }
        });
    });
    // 3. Аналіз документа для діагностики
    function analyzeDocument(document) {
        if (document.languageId !== 'mylang') {
            return;
        }
        const diagnostics = [];
        const text = document.getText();
        const lines = text.split('\n');
        // Приклад аналізу: шукаємо некоректне використання "function" без назви
        lines.forEach((line, index) => {
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('function') && !trimmedLine.match(/function\s+\w+/)) {
                const range = new vscode.Range(
                    index, line.indexOf('function'),
                    index, line.indexOf('function') + 'function'.length
                );
                const diagnostic = new vscode.Diagnostic(
                    range,
                    'Function keyword must be followed by a name',
                    vscode.DiagnosticSeverity.Error
                );
                diagnostic.code = 'invalid-function';
                diagnostics.push(diagnostic);
            }
            // Шукаємо "print" без аргументів
            if (trimmedLine.match(/print\s*\(\s*\)/)) {
                const matchIndex = line.indexOf('print');
                const range = new vscode.Range(
                    index, matchIndex,
                    index, matchIndex + 'print'.length
                );
                const diagnostic = new vscode.Diagnostic(
                    range,
                    'Print function requires at least one argument',
                    vscode.DiagnosticSeverity.Warning
                );
                diagnostic.code = 'empty-print';
                diagnostics.push(diagnostic);
            }
        });
        // Оновлюємо діагностику
        diagnosticCollection.set(document.uri, diagnostics);
    }
    // 4. Реєструємо обробник зміни документа
    const changeDocumentSubscription = vscode.workspace.onDidChangeTextDocument(event => {
        analyzeDocument(event.document);
    });
    // 5. Аналізуємо відкритий документ
    const openDocumentSubscription = vscode.workspace.onDidOpenTextDocument(document => {
        analyzeDocument(document);
    });
    // Аналізуємо активний документ при запуску
    if (vscode.window.activeTextEditor) {
        analyzeDocument(vscode.window.activeTextEditor.document);
    }
    // Реєструємо всі ресурси
    context.subscriptions.push(
        completionProvider,
        uppercaseCommand,
        changeDocumentSubscription,
        openDocumentSubscription,
        diagnosticCollection
    );
}
function deactivate() {
    diagnosticCollection.clear();
}
module.exports = {
    activate,
    deactivate
};