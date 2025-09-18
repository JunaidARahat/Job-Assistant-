from app.scraper.provider import LinkedInProvider

def test_linkedin_parse():
    p = LinkedInProvider(samples_dir='data/samples/linkedin')
    jobs = p.fetch()
    assert isinstance(jobs, list)
    assert len(jobs) >= 1
    j = jobs[0]
    assert 'title' in j and 'company' in j and 'requirements' in j
