# Token

1. [Github "Personal access tokens"](https://github.com/settings/tokens) --> "Generate new token" --> scope "Full control of private repositories"
2. Put the token in environment variable `GITHUB_TOKEN`. For example, add to `~/.bash_profile` or `~/.bashrh`: `export GITHUB_TOKEN="my-github-token"`

# REST API v3

Documentation: https://developer.github.com/v3/

- [List endpoints](https://developer.github.com/v3/#root-endpoint): `$ curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com`
- [Get the authenticated user](https://developer.github.com/v3/users/#get-the-authenticated-user): `$ curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user`
- [Search](https://developer.github.com/v3/search/):
    - [Search code](https://developer.github.com/v3/search/#search-code). For example:
        - List repositories in organization `foo` that have file `my-file.ext` (the `awk` command removes duplicates without sorting):
            ```sh
            $ curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/search/code?q=org:foo+filename:my-file.ext | jq .items | jq -r '.[].repository.html_url' | awk '!x[$0]++'
            ```
