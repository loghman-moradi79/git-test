# Weblog Repository
___
This Respo is for session Weblog
___

## `code`

```json
{
  "fristname": "Loghman",
  "lastname": "Moradi",
  "username": "loghman_79"
}
```
## Default Usage
```python
def information_authors(request, author_id):
    author = get_object_or_404(Account, id=author_id)
    user = author.user
    posts = Post.published.filter(author=user)
    context = {
        'author': author,
        'posts': posts,
    }
    return render(request, 'forms/information.html', context)
```

___
## Lists:
Ordered:

1. python
2. npm
3. react
4. django

Unordered:
- FrontEnd (`Html` `Css` `Js` => Package)
    - react
    - html
    - css
___


___
## Project List

[weblog](https://github.com/loghman-moradi79/)

## Image
![persepolis](https://upload.wikimedia.org/wikipedia/en/thumb/0/05/FC_Persepolis_Official_Logo.svg/300px-FC_Persepolis_Official_Logo.svg.png)
___