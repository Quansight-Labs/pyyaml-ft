import pytest

import yaml
from .utils import filter_data_files

# Tokens mnemonic:
# directive:            %
# document_start:       ---
# document_end:         ...
# alias:                *
# anchor:               &
# tag:                  !
# scalar                _
# block_sequence_start: [[
# block_mapping_start:  {{
# block_end:            ]}
# flow_sequence_start:  [
# flow_sequence_end:    ]
# flow_mapping_start:   {
# flow_mapping_end:     }
# entry:                ,
# key:                  ?
# value:                :

_replaces = {
    yaml.DirectiveToken: '%',
    yaml.DocumentStartToken: '---',
    yaml.DocumentEndToken: '...',
    yaml.AliasToken: '*',
    yaml.AnchorToken: '&',
    yaml.TagToken: '!',
    yaml.ScalarToken: '_',
    yaml.BlockSequenceStartToken: '[[',
    yaml.BlockMappingStartToken: '{{',
    yaml.BlockEndToken: ']}',
    yaml.FlowSequenceStartToken: '[',
    yaml.FlowSequenceEndToken: ']',
    yaml.FlowMappingStartToken: '{',
    yaml.FlowMappingEndToken: '}',
    yaml.BlockEntryToken: ',',
    yaml.FlowEntryToken: ',',
    yaml.KeyToken: '?',
    yaml.ValueToken: ':',
}


@pytest.mark.parametrize("data_filename,tokens_filename", filter_data_files(".data", ".tokens"))
def test_tokens(data_filename, tokens_filename):
    tokens1 = []
    with open(tokens_filename, 'r') as file:
        tokens2 = file.read().split()
    with open(data_filename, 'rb') as file:
        for token in yaml.scan(file):
            if not isinstance(token, (yaml.StreamStartToken, yaml.StreamEndToken)):
                tokens1.append(_replaces[token.__class__])
    assert len(tokens1) == len(tokens2), (tokens1, tokens2)
    for token1, token2 in zip(tokens1, tokens2):
        assert token1 == token2, (token1, token2)


@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_scanner(data_filename, canonical_filename):
    for filename in [data_filename, canonical_filename]:
        tokens = []
        with open(filename, 'rb') as file:
            for token in yaml.scan(file):
                tokens.append(token.__class__.__name__)
