import re

import yaml
from ansible.errors import AnsibleFilterError
from ansible.module_utils._text import to_native, to_text
from ansible.parsing.yaml.dumper import AnsibleDumper


class FilterModule(object):

    class NiceDumper(AnsibleDumper):
        _str_pattern = re.compile(r'^[\w\.]+$')

    def __init__(self) -> None:

        def repr_str(dumper, data):
            if '\n' in data:
                return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
            if not re.match(self.NiceDumper._str_pattern, data):
                # quote string scalars, if they contain characters which are not [\w\.]
                return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='"')
            return dumper.represent_scalar(u'tag:yaml.org,2002:str', data)

        self.NiceDumper.add_representer(str, repr_str)

    def filters(self):
        return {
            'to_very_nice_yaml': self.to_very_nice_yaml,
        }

    def to_very_nice_yaml(self, value, indent=2, *args, **kw):
        '''Make verbose, human readable yaml with block style for multiline strings.'''
        try:
            transformed = yaml.dump(
                value,
                Dumper=self.NiceDumper,
                indent=indent,
                width=9999999,
                allow_unicode=True,
                default_flow_style=False,
                **kw,
            )
        except Exception as e:
            raise AnsibleFilterError('to_very_nice_yaml - {}'.format(to_native(e)), orig_exc=e)
        return to_text(transformed)
