"""Other / miscellaneous platform adapters."""

from __future__ import annotations

from uscan.platforms.base import Platform


class Patreon(Platform):
    name = "Patreon"
    category = "other"
    url_pattern = "https://www.patreon.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["not exist", "404"]
    found_indicators = ["patreon.com", "creator-profile"]


class BuyMeACoffee(Platform):
    name = "Buy Me a Coffee"
    category = "other"
    url_pattern = "https://www.buymeacoffee.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["Page not found", "404"]
    found_indicators = ["buymeacoffee.com", "supporter"]


class ProductHunt(Platform):
    name = "Product Hunt"
    category = "other"
    url_pattern = "https://www.producthunt.com/@{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,20}$"
    max_length = 20
    not_found_indicators = ["Page not found"]
    found_indicators = ["producthunt.com", "profile"]


class Hackernews(Platform):
    name = "Hacker News"
    category = "other"
    url_pattern = "https://news.ycombinator.com/user?id={username}"
    username_regex = r"^[a-zA-Z0-9_-]{2,15}$"
    min_length = 2
    max_length = 15
    not_found_indicators = ["No such user"]
    found_indicators = ["user?id=", "created:"]


class Keybase(Platform):
    name = "Keybase"
    category = "other"
    url_pattern = "https://keybase.io/{username}"
    username_regex = r"^[a-zA-Z0-9_]{2,16}$"
    min_length = 2
    max_length = 16
    not_found_indicators = ["not found"]
    found_indicators = ["keybase.io", "profile"]


class Fiverr(Platform):
    name = "Fiverr"
    category = "professional"
    url_pattern = "https://www.fiverr.com/{username}"
    username_regex = r"^[a-zA-Z0-9_]{3,15}$"
    min_length = 3
    max_length = 15
    not_found_indicators = ["page you requested is no longer available"]
    found_indicators = ["fiverr.com", "seller-card"]


class Imgur(Platform):
    name = "Imgur"
    category = "content"
    url_pattern = "https://imgur.com/user/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Zoinks! You've taken a wrong turn"]
    found_indicators = ["imgur.com", "points"]


class Giphy(Platform):
    name = "Giphy"
    category = "content"
    url_pattern = "https://giphy.com/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Page Not Found"]
    found_indicators = ["giphy.com", "profile"]


class Wikipedia(Platform):
    name = "Wikipedia"
    category = "other"
    url_pattern = "https://en.wikipedia.org/wiki/User:{username}"
    username_regex = r"^[a-zA-Z0-9_ ]{1,40}$"
    max_length = 40
    not_found_indicators = ["does not have a user page"]
    found_indicators = ["wikipedia.org", "mw-parser-output"]


class HuggingFace(Platform):
    name = "Hugging Face"
    category = "developer"
    url_pattern = "https://huggingface.co/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,40}$"
    max_length = 40
    not_found_indicators = ["Page Not Found"]
    found_indicators = ["huggingface.co", "avatar"]


class NPM(Platform):
    name = "npm"
    category = "developer"
    url_pattern = "https://www.npmjs.com/~{username}"
    username_regex = r"^[a-z0-9._-]{1,40}$"
    max_length = 40
    not_found_indicators = ["404 - page not found"]
    found_indicators = ["npmjs.com", "profile"]


class PyPI(Platform):
    name = "PyPI"
    category = "developer"
    url_pattern = "https://pypi.org/user/{username}/"
    username_regex = r"^[a-zA-Z0-9._-]{1,50}$"
    max_length = 50
    not_found_indicators = ["Page Not Found"]
    found_indicators = ["pypi.org/user", "profile"]


class Hashnode(Platform):
    name = "Hashnode"
    category = "content"
    url_pattern = "https://hashnode.com/@{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,30}$"
    max_length = 30
    not_found_indicators = ["not found", "404"]
    found_indicators = ["hashnode.com", "profile"]


class GitHubGist(Platform):
    name = "GitHub Gist"
    category = "developer"
    url_pattern = "https://gist.github.com/{username}"
    username_regex = r"^[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,37}[a-zA-Z0-9])?$"
    max_length = 39
    not_found_indicators = ["Not Found"]
    found_indicators = ["gist.github.com", "avatar"]


class DockerHub(Platform):
    name = "Docker Hub"
    category = "developer"
    url_pattern = "https://hub.docker.com/u/{username}"
    username_regex = r"^[a-z0-9][a-z0-9_.-]{0,29}$"
    max_length = 30
    not_found_indicators = ["HttpError"]
    found_indicators = ["hub.docker.com", "user-repo-list"]


class Tryhackme(Platform):
    name = "TryHackMe"
    category = "other"
    url_pattern = "https://tryhackme.com/p/{username}"
    username_regex = r"^[a-zA-Z0-9_]{1,20}$"
    max_length = 20
    not_found_indicators = ["not found", "404"]
    found_indicators = ["tryhackme.com", "profile"]


class HackTheBox(Platform):
    name = "Hack The Box"
    category = "other"
    url_pattern = "https://app.hackthebox.com/users/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,20}$"
    max_length = 20
    not_found_indicators = ["not found"]
    found_indicators = ["hackthebox", "profile"]


class Disqus(Platform):
    name = "Disqus"
    category = "other"
    url_pattern = "https://disqus.com/by/{username}/"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Page not found"]
    found_indicators = ["disqus.com/by", "user-profile"]


class GoodReads(Platform):
    name = "Goodreads"
    category = "other"
    url_pattern = "https://www.goodreads.com/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["Page not found"]
    found_indicators = ["goodreads.com", "userProfileLeftContainer"]


class Instructables(Platform):
    name = "Instructables"
    category = "other"
    url_pattern = "https://www.instructables.com/member/{username}/"
    username_regex = r"^[a-zA-Z0-9_-]{1,30}$"
    max_length = 30
    not_found_indicators = ["404 Not Found"]
    found_indicators = ["instructables.com/member", "member-profile"]


class Mixcloud(Platform):
    name = "Mixcloud"
    category = "content"
    url_pattern = "https://www.mixcloud.com/{username}/"
    username_regex = r"^[a-zA-Z0-9_-]{1,25}$"
    max_length = 25
    not_found_indicators = ["Page not found"]
    found_indicators = ["mixcloud.com", "profile"]


class Letterboxd(Platform):
    name = "Letterboxd"
    category = "content"
    url_pattern = "https://letterboxd.com/{username}/"
    username_regex = r"^[a-zA-Z0-9_]{1,15}$"
    max_length = 15
    not_found_indicators = ["Error: Not Found"]
    found_indicators = ["letterboxd.com", "body-content"]


class Last_FM(Platform):
    name = "Last.fm"
    category = "content"
    url_pattern = "https://www.last.fm/user/{username}"
    username_regex = r"^[a-zA-Z0-9_-]{2,15}$"
    min_length = 2
    max_length = 15
    not_found_indicators = ["User not found"]
    found_indicators = ["last.fm/user", "user-header"]


OTHER_PLATFORMS: list[type[Platform]] = [
    Patreon, BuyMeACoffee, ProductHunt, Hackernews, Keybase,
    Fiverr, Imgur, Giphy, Wikipedia, HuggingFace, NPM, PyPI,
    Hashnode, GitHubGist, DockerHub, Tryhackme, HackTheBox,
    Disqus, GoodReads, Instructables, Mixcloud, Letterboxd, Last_FM,
]
