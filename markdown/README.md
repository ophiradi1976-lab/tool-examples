## Markdown Utils

###  Markdown to HTML
```
brew install pandoc
brew install mdcat
```

* View MD as html (render in terminal) 
```
mdcat file.md
```

* Translate MD to HTML
```
pandoc ~/todo_family.md -o /tmp/ideas.html
open /tmp/ideas.html
```
