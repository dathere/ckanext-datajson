import logging

log = logging.getLogger(__name__)


class TestDataJsonValidation(object):

    def test_data_json_validator_route(self, app):
        ''' Test that route returns 200 '''

        res = app.get('/pod/validate')

        assert res.status_code == 200
        assert 'Validate a DCAT-US /data.json File' in res.body

    def test_data_json_without_url(self, app):
        ''' Test that a valid data.json passes '''

        res = app.post('/pod/validate')

        assert res.status_code == 200
        assert 'Bad Request' in res.body
        assert 'Please send a post request with &#39;url&#39; in the payload' in res.body

        res = app.post('/pod/validate', data={'url2': 'data.gov'})

        assert res.status_code == 200
        assert 'Bad Request' in res.body
        assert 'Please send a post request with &#39;url&#39; in the payload' in res.body

    def test_data_json_valid(self, app):
        ''' Test that a valid data.json passes '''

        res = app.post('/pod/validate', data={
            'url': ('https://raw.githubusercontent.com/GSA/ckanext-datajson/main/ckanext/datajson/tests/datajson-samples/'
                    'collection-1-parent-2-children.data.json')
        })

        assert res.status_code == 200
        assert 'No Errors' in res.body
        assert 'Great job!' in res.body

    def test_data_json_bad_link(self, app):
        ''' Test that a bad link fails '''

        res = app.post('/pod/validate', data={'url': 'data.gov'})

        assert res.status_code == 200
        assert 'Invalid JSON' in res.body
        assert 'The file does not meet basic JSON syntax requirements' in res.body

    def test_data_json_missing_dataset_fields(self, app):
        ''' Test that an invalid data.json that is missing dataset fields fails '''

        res = app.post('/pod/validate', data={
            'url': ('https://raw.githubusercontent.com/GSA/ckanext-datajson/datajson-validator/ckanext/datajson/'
                    'tests/datajson-samples/missing-dataset-fields.data.json')
        })

        assert res.status_code == 200
        assert 'Dataset ➡ 0 has a problem' in res.body
        assert '&#39;accessLevel&#39; is a required property.' in res.body
        assert '&#39;bureauCode&#39; is a required property.' in res.body
        assert '&#39;contactPoint&#39; is a required property.' in res.body
        assert '&#39;description&#39; is a required property.' in res.body
        assert '&#39;identifier&#39; is a required property.' in res.body
        assert '&#39;keyword&#39; is a required property.' in res.body
        assert '&#39;modified&#39; is a required property.' in res.body
        assert '&#39;programCode&#39; is a required property.' in res.body
        assert '&#39;publisher&#39; is a required property.' in res.body
        assert '&#39;title&#39; is a required property.' in res.body
        assert 'Dataset ➡ 1 has a problem' in res.body
        assert '&#39;description&#39; is a required property.' in res.body

    def test_data_json_missing_catalog_fields(self, app):
        ''' Test that an invalid data.json that is missing catalog fields fails '''

        res = app.post('/pod/validate', data={
            'url': ('https://raw.githubusercontent.com/GSA/ckanext-datajson/datajson-validator/ckanext/datajson/'
                    'tests/datajson-samples/missing-catalog.data.json')
        })

        assert res.status_code == 200
        assert 'The root of data.json has a problem' in res.body
        assert '&#39;conformsTo&#39; is a required property.' in res.body
        assert '@context has a problem' in res.body
        assert '&#39;project-open-data.cio.gov/v1.1/schema&#39; is not a &#39;uri&#39;.' in res.body
        assert '@type has a problem' in res.body
        assert '&#39;dcat:Test&#39; is not one of [&#39;dcat:Catalog&#39;].' in res.body
        assert 'describedBy has a problem' in res.body
        assert '&#39;data.gov&#39; is not a &#39;uri&#39;.'


    def test_data_json_unresolvable(self, app):

        res = app.post('/pod/validate', data={
            'url': 'http://some.unresolvable.hostname.fer-reals/data.json'
        })

        assert res.status_code == 200
        assert 'Error Loading File' in res.body
        assert 'The address could not be loaded' in res.body

        res = app.post('/pod/validate', data={
            'url': 'https://www.google.com:443/data.json'
        })

        assert res.status_code == 200
        assert 'Error Loading File' in res.body
        assert 'The address could not be loaded' in res.body
        assert 'HTTP Error 404' in res.body
