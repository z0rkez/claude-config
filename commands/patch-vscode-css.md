Восстанови оранжевую иконку VS Code после обновления.

## Контекст (не нужно переоткрывать)

- VS Code установлен в `/opt/visual-studio-code`
- Файл для патча: `/opt/visual-studio-code/resources/app/out/vs/code/electron-browser/workbench/workbench.html`
- CSS с оранжевой иконкой: `/home/zorkez/.config/Code/User/custom.css`
- Расширение `be5invis.vscode-custom-css` встраивает CSS как `<style>` тег перед `</html>`, предварительно удаляя CSP мета-тег
- Скрипт патча уже создан: `/home/zorkez/patch-vscode.py`

## Что нужно сделать

1. Убедиться что `/home/zorkez/patch-vscode.py` существует. Если нет — создать его с содержимым:

```python
#!/usr/bin/env python3
import re

html_path = '/opt/visual-studio-code/resources/app/out/vs/code/electron-browser/workbench/workbench.html'
css_path = '/home/zorkez/.config/Code/User/custom.css'

with open(html_path, 'r') as f:
    html = f.read()

with open(html_path + '.bak', 'w') as f:
    f.write(html)

html = re.sub(r'<!-- !! VSCODE-CUSTOM-CSS-START !! -->[\s\S]*?<!-- !! VSCODE-CUSTOM-CSS-END !! -->\n*', '', html)
html = re.sub(r'<!-- !! VSCODE-CUSTOM-CSS-SESSION-ID [\w-]+ !! -->\n*', '', html)
html = re.sub(r'<meta\s+http-equiv="Content-Security-Policy"[\s\S]*?/>', '', html)

with open(css_path, 'r') as f:
    css = f.read()

inject = (
    '<!-- !! VSCODE-CUSTOM-CSS-SESSION-ID manual-inject !! -->\n'
    '<!-- !! VSCODE-CUSTOM-CSS-START !! -->\n'
    '<style>' + css + '</style>\n'
    '<!-- !! VSCODE-CUSTOM-CSS-END !! -->\n'
)

html = html.replace('</html>', inject + '</html>')

with open(html_path, 'w') as f:
    f.write(html)

print('Готово! Перезапусти VS Code.')
```

2. Сообщить пользователю запустить команду (sudo требует терминал, напрямую запустить нельзя):

```
! sudo python3 ~/patch-vscode.py
```

3. Напомнить перезапустить VS Code после выполнения.
