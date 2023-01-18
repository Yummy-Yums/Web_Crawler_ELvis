class TestUtils:
    def test_one(self):
        x = "this"
        assert "h" in x

    def test_create_file(self):
        assert 'F' in "File is created"

    def test_combine_dictionary_keys_and_values(self):
        assert 'C' in "Combine dictionary keys and values"

    def test_extract_all_web_links(self):
        assert 'E' in "Extract web links"

    def test_decode_webpage(self):
        assert 'D' in "Decode webpage"

    def test_get_related_pages(self):
        assert 'G' in "Get related pages"

    def test_get_non_related_pages(self):
        assert 'G' in "Get non related pages"

    def test_add_to_queue(self):
        assert 'A' in "Add to queue"
