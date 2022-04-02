"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>> is_http_domain('http://wikipedia.org')
    True
    >>> is_http_domain('https://ru.wikipedia.org/')
    True
    >>> is_http_domain('griddynamics.com')
    False
"""
import re


def is_http_domain(domain: str) -> bool:
    for i in ["http://", "https://"]:
        result = re.match(i, domain)
        if bool(result):
            return True
    return False


"""
write tests for is_http_domain function
"""
def test_is_http_domain():
    assert is_http_domain('http://wikipedia.org') == True

def test_is_http_domain_false():
    assert is_http_domain('griddynamics.com') == False