from urlparse import urlparse, parse_qs

from django import test
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse

import mock
import requests
from nose.tools import eq_

from lib.bango.constants import HEADERS_SERVICE_GET
from lib.bango.tests import samples
from lib.boku.client import get_boku_request_signature


class Proxy(test.TestCase):

    def setUp(self):
        request = mock.patch('lib.proxy.views.requests', name='test.proxy')
        self.req = request.start()
        self.req.exceptions = requests.exceptions
        self.req.patcher = request
        self.addCleanup(request.stop)


@mock.patch.object(settings, 'SOLITUDE_PROXY', True)
@mock.patch.object(settings, 'BANGO_AUTH', {'USER': 'me', 'PASSWORD': 'shh'})
class TestBango(Proxy):

    def setUp(self):
        super(TestBango, self).setUp()
        self.url = reverse('bango.proxy')

    def test_not_present(self):
        with self.assertRaises(KeyError):
            self.client.post(self.url, samples.sample_request,
                             **{'content_type': 'text/xml'})

    def test_header(self):
        self.client.post(self.url,
                         samples.sample_request,
                         **{'content_type': 'text/xml',
                            HEADERS_SERVICE_GET: 'http://url.com/b',
                            'HTTP_X_SOLITUDE_SOAPACTION': 'foo'})
        eq_(self.req.post.call_args[1]['headers']['SOAPAction'], 'foo')

    def test_good(self):
        self.client.post(self.url,
                         samples.sample_request,
                         **{'content_type': 'text/xml',
                            HEADERS_SERVICE_GET: 'http://url.com/b'})
        body = self.req.post.call_args[1]['data']
        assert '<ns0:username>me</ns0:username>' in body
        assert '<ns0:password>shh</ns0:password>' in body

    def test_billing(self):
        self.client.post(self.url,
                         samples.billing_request,
                         **{'content_type': 'text/xml',
                            HEADERS_SERVICE_GET: 'http://url.com/b'})
        body = self.req.post.call_args[1]['data']
        assert '<ns1:username>me</ns1:username>' in body
        assert '<ns1:password>shh</ns1:password>' in body

    def test_refund(self):
        self.client.post(self.url,
                         samples.refund_request,
                         **{'content_type': 'text/xml',
                            HEADERS_SERVICE_GET: 'http://url.com/b'})
        body = self.req.post.call_args[1]['data']
        assert '<ns0:username>me</ns0:username>' in body
        assert '<ns0:password>shh</ns0:password>' in body


@mock.patch.object(settings, 'SOLITUDE_PROXY', True)
@mock.patch.object(
    settings, 'ZIPPY_CONFIGURATION',
    {'f': {'url': 'http://f.c', 'auth': {'key': 'k', 'secret': 's'}}})
class TestProvider(Proxy):

    def setUp(self):
        super(TestProvider, self).setUp()
        self.url = (reverse('provider.proxy', kwargs={'reference_name': 'f'})
                    + '/f/b/')

    def test_not_setup(self):
        with self.settings(ZIPPY_CONFIGURATION={}):
            with self.assertRaises(ImproperlyConfigured):
                self.client.get(self.url)

    def test_call(self):
        self.client.get(self.url)
        args = self.req.get.call_args
        assert 'OAuth realm' in args[1]['headers']['Authorization']
        eq_(args[0][0], 'http://f.c/f/b/')

    def test_type(self):
        self.client.get(self.url, CONTENT_TYPE='t/c', HTTP_ACCEPT='t/c')
        eq_(self.req.get.call_args[1]['headers']['Content-Type'], 't/c')
        eq_(self.req.get.call_args[1]['headers']['Accept'], 't/c')

    def test_post(self):
        self.client.post(self.url, data={'foo': 'bar'})
        assert 'foo' in self.req.post.call_args[1]['data']

    def test_get(self):
        self.client.get(self.url, data={'baz': 'quux'})
        assert '?baz=quux' in self.req.get.call_args[0][0]


@mock.patch.object(settings, 'SOLITUDE_PROXY', True)
@mock.patch.object(
    settings, 'ZIPPY_CONFIGURATION',
    {'boku': {'url': 'http://f.c', 'auth': {'secret': 's', 'key': 'f'}}})
class TestBoku(Proxy):

    def setUp(self):
        super(TestBoku, self).setUp()
        self.url = reverse('provider.proxy', kwargs={'reference_name': 'boku'})
        self.billing = self.url + 'billing/request?f=b'
        self.sig = self.url + 'check_sig?f=b&sig={0}'

    def test_call(self):
        self.client.get(self.billing)

        sig = parse_qs(urlparse(self.req.get.call_args[0][0]).query)['sig']
        assert sig, 'A sig parameter should have been added'

    def test_good_sig(self):
        sig = get_boku_request_signature(settings.BOKU_SECRET_KEY, {'f': 'b'})
        eq_(self.client.get(self.sig.format(sig)).status_code, 204)

    def test_bad_sig(self):
        eq_(self.client.get(self.sig.format('bad')).status_code, 400)
