const vscode = require('vscode');
const fs = require('fs');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	let disposable = vscode.commands.registerCommand('testingliveview.LiveView', function () {
		
		const editor = vscode.window.activeTextEditor;
		if (editor) {
			const filePath = editor.document.fileName;
   			const svgContent = fs.readFileSync(filePath, 'utf-8');

			const panel = vscode.window.createWebviewPanel(
				'svgPreview',
				'SVG Preview',
				vscode.ViewColumn.Beside,
				{}
			);
			 
			panel.webview.html = getWebviewContent(svgContent);
		} else {
			vscode.window.showErrorMessage("No file is opened.");
		}
	});

	context.subscriptions.push(disposable);
}

function getWebviewContent(svgContent) {
	return `
   <html>
	 <body>
	   <div>
		 ${svgContent}
	   </div>
	 </body>
   </html>
	`;
  }

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
