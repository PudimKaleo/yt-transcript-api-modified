class _TranscriptParser:
    _FORMATTING_TAGS = [
        "strong",  # important
        "em",  # emphasized
        "b",  # bold
        "i",  # italic
        "mark",  # marked
        "small",  # smaller
        "del",  # deleted
        "ins",  # inserted
        "sub",  # subscript
        "sup",  # superscript
    ]

    def __init__(self, preserve_formatting: bool = False):
        self._html_regex = self._get_html_regex(preserve_formatting)

    def _get_html_regex(self, preserve_formatting: bool) -> Pattern[str]:
        if preserve_formatting:
            formats_regex = "|".join(self._FORMATTING_TAGS)
            formats_regex = r"<\/?(?!\/?(" + formats_regex + r")\b).*?\b>"
            html_regex = re.compile(formats_regex, re.IGNORECASE)
        else:
            html_regex = re.compile(r"<[^>]*>", re.IGNORECASE)
        return html_regex

    def parse(self, raw_data: str, start_time: float = 0) -> List[FetchedTranscriptSnippet]:
        """
        Parses the raw transcript data and filters snippets based on the start_time.
        :param raw_data: the raw XML transcript data
        :param start_time: the timestamp (in seconds) from which to start extracting captions
        :return: a list of FetchedTranscriptSnippet objects
        """
        return [
            FetchedTranscriptSnippet(
                text=re.sub(self._html_regex, "", unescape(xml_element.text)),
                start=float(xml_element.attrib["start"]),
                duration=float(xml_element.attrib.get("dur", "0.0")),
            )
            for xml_element in ElementTree.fromstring(raw_data)
            if xml_element.text is not None and float(xml_element.attrib["start"]) >= start_time
        ]
