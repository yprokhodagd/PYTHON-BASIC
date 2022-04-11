from practice.p6_web_scraping.stock_info import get_companies, _fill_table1


def test_response_code_200():
    companies = get_companies()
    assert type(companies) == list
    assert len(companies) == 25


def test_fill_table1():
    HEADERS = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/99.0.4844.84 Safari/537.36"}
    assert _fill_table1('AMD', 'AMD') == [['AMD', 'AMD', 'United States', '15,500', 'Mr. Devinder  Kumar', '1956']]
