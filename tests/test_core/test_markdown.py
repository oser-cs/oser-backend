import os
from django.test import TestCase
from core.markdown import extract_md_file_refs


class ExtractFileRefsTest(TestCase):
    """Test the extract_md_file_refs function."""

    texts = [
        'Here is my home: ![home](path/to/home.png).',
        'You can find it [here](www.findme.com).',
    ]

    def assertExtracts(self, text, expected):
        extracted = extract_md_file_refs(text)
        extracted_filenames = [ref.filename for ref in extracted]
        self.assertListEqual(extracted_filenames, list(expected))

    def test_empty_text(self):
        self.assertExtracts('', [])

    def test_image_file(self):
        md = 'Here is my home: ![home](home.png).'
        self.assertExtracts(md, ['home.png'])

    def test_image_file_full_path(self):
        path = os.path.join('path', 'to', 'home.png')
        md = 'Here is my home: ![home]({}).'.format(path)
        self.assertExtracts(md, ['home.png'])

    def test_does_not_mind_urls(self):
        md = 'You can find it [here](http://www.findithere.com)'
        self.assertExtracts(md, ['www.findithere.com'])


# TODO test MdFileRef class
# TODO test extract_image_refs
# TODO test add_domain_to_image_files
# TODO test _get_domain
